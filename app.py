import csv
import io
import os
import time
from datetime import date, datetime

import requests
import streamlit as st


st.set_page_config(page_title="EduTrack AI", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")

STATUS_LABELS = {
    "pending": "Pendente",
    "in_progress": "Em andamento",
    "completed": "Concluída",
}

STATUS_VALUES = {label: value for value, label in STATUS_LABELS.items()}

PRIORITY_LABELS = {
    "low": "Baixa",
    "medium": "Média",
    "high": "Alta",
}

PRIORITY_VALUES = {label: value for value, label in PRIORITY_LABELS.items()}


class ApiRequestError(RuntimeError):
    def __init__(self, message, status_code=None, url=None):
        super().__init__(message)
        self.status_code = status_code
        self.url = url


def get_secret(name, default=""):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


def get_base_url(path=""):
    path = path.lstrip("/")
    if path.startswith("auth/"):
        specific_key = "XANO_AUTH_BASE_URL"
    elif path.startswith("user/") or path.startswith("account"):
        specific_key = "XANO_MEMBERS_ACCOUNTS_BASE_URL"
    elif path.startswith("subjects"):
        specific_key = "XANO_SUBJECTS_BASE_URL"
    elif path.startswith("tasks"):
        specific_key = "XANO_TASKS_BASE_URL"
    else:
        specific_key = "XANO_BASE_URL"

    env_url = os.getenv(specific_key, "")
    if env_url:
        return env_url.rstrip("/")

    secret_url = get_secret(specific_key, "")
    if secret_url:
        return secret_url.rstrip("/")

    if path.startswith("subjects"):
        members_url = os.getenv("XANO_MEMBERS_ACCOUNTS_BASE_URL", "") or get_secret("XANO_MEMBERS_ACCOUNTS_BASE_URL", "")
        return members_url.rstrip("/") if members_url else ""

    if path.startswith("tasks"):
        members_url = os.getenv("XANO_MEMBERS_ACCOUNTS_BASE_URL", "") or get_secret("XANO_MEMBERS_ACCOUNTS_BASE_URL", "")
        return members_url.rstrip("/") if members_url else ""

    fallback_url = os.getenv("XANO_BASE_URL", "") or get_secret("XANO_BASE_URL", "")
    return fallback_url.rstrip("/") if fallback_url else ""


def init_state():
    defaults = {
        "auth_token": None,
        "auth_expires_at": 0,
        "user": None,
        "auth_mode": "login",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def is_authenticated():
    token = st.session_state.get("auth_token")
    expires_at = st.session_state.get("auth_expires_at", 0)
    if token and expires_at and time.time() >= expires_at:
        logout("Sua sessão expirou. Faça login novamente.")
        return False
    return bool(token)


def logout(message=None):
    st.session_state.auth_token = None
    st.session_state.auth_expires_at = 0
    st.session_state.user = None
    if message:
        st.warning(message)


def api_request(method, path, payload=None, params=None):
    base_url = get_base_url(path)
    if not base_url:
        raise RuntimeError("Configure a URL base do grupo Xano para este endpoint.")

    headers = {"Content-Type": "application/json"}
    if st.session_state.get("auth_token"):
        headers["Authorization"] = f"Bearer {st.session_state.auth_token}"

    response = requests.request(
        method,
        f"{base_url}/{path.lstrip('/')}",
        json=payload,
        params=params,
        headers=headers,
        timeout=20,
    )
    if response.status_code == 401:
        logout("Sua sessão expirou. Faça login novamente.")
        st.rerun()
    if response.status_code >= 400:
        try:
            message = response.json().get("message") or response.json().get("error")
        except ValueError:
            message = response.text
        # Log detailed info to terminal for debugging
        debug_msg = f"API request error: {response.status_code} {response.reason} -> {message}\nURL: {response.url}"
        print(debug_msg)
        raise ApiRequestError(
            message or f"Erro ao conectar com o Xano. (HTTP {response.status_code})",
            status_code=response.status_code,
            url=response.url,
        )
    if response.status_code == 204 or not response.content:
        return None
    return response.json()


def normalize_list(response):
    if response is None:
        return []
    if isinstance(response, list):
        return response
    if isinstance(response, dict):
        data = response.get("data", response)
        if isinstance(data, dict) and "items" in data:
            return data["items"]
        if isinstance(data, dict) and "subjects" in data:
            return data["subjects"]
        if isinstance(data, list):
            return data
    return []


def normalize_user(response):
    if isinstance(response, dict):
        data = response.get("data", response)
        if isinstance(data, dict):
            return data
    return {}


def parse_due(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).date()
    except ValueError:
        return None


def is_overdue(task):
    due_date = parse_due(task.get("due_date"))
    return bool(due_date and due_date < date.today() and task.get("status") != "completed")


def overdue_task_count_for_subject(subject_id, tasks):
    return sum(
        1
        for task in tasks
        if task.get("subject_id") == subject_id and is_overdue(task)
    )


def fetch_subjects(include_archived=False):
    params = {"archived": include_archived, "include_inactive": include_archived}
    try:
        return normalize_list(api_request("GET", "subjects", params=params))
    except ApiRequestError as exc:
        if exc.status_code == 404 or "unable to locate request" in str(exc).lower():
            st.warning("Endpoint /subjects não encontrado no Xano. Gere/push os arquivos em apis/members_accounts ou configure XANO_SUBJECTS_BASE_URL.")
            return []
        raise


def fetch_tasks(status=None):
    if not get_base_url("tasks"):
        return []

    params = {}
    if status:
        params["status"] = status
    try:
        response = api_request("GET", "tasks", params=params)
    except ApiRequestError as exc:
        if exc.status_code == 404 or "unable to locate request" in str(exc).lower():
            st.warning("Endpoint /tasks não encontrado no Xano. Gere/push os arquivos em apis/members_accounts ou configure XANO_TASKS_BASE_URL.")
            return []
        raise
    return [normalize_task(task) for task in normalize_list(response)]


def fetch_current_user():
    try:
        st.session_state.user = normalize_user(api_request("GET", "auth/me"))
    except RuntimeError:
        st.session_state.user = None


def subject_is_archived(subject):
    if "archived" in subject:
        return bool(subject.get("archived"))
    if "is_active" in subject:
        return not bool(subject.get("is_active"))
    return False


def build_subject_code(name, subject_id=None):
    base = "".join(char for char in (name or "disciplina").upper() if char.isalnum())[:12] or "DISCIPLINA"
    if subject_id:
        return f"{base[:8]}{subject_id}"[:20]
    return f"{base}{int(time.time()) % 10000}"[:20]


def get_current_account_id():
    user = st.session_state.get("user") or {}
    return user.get("account_id")


def normalize_task(task):
    normalized = dict(task)
    if "subject_id" not in normalized and "subject" in normalized:
        normalized["subject_id"] = normalized.get("subject")
    normalized.setdefault("priority", "medium")
    normalized.setdefault("status", "pending")
    return normalized


def due_group_label(task):
    due_date = parse_due(task.get("due_date"))
    if not due_date:
        return "Sem prazo"
    if is_overdue(task):
        return "Vencidas"
    if due_date == date.today():
        return "Hoje"
    if due_date > date.today() and (due_date - date.today()).days <= 7:
        return "Próximos 7 dias"
    return due_date.strftime("%d/%m/%Y")


def task_progress(tasks):
    if not tasks:
        return 0
    completed = [task for task in tasks if task.get("status") == "completed"]
    return round((len(completed) / len(tasks)) * 100)


def tasks_for_subject(subject_id, tasks):
    return [task for task in tasks if task.get("subject_id") == subject_id]


def has_duplicate_subject(subjects, name, professor, ignore_id=None):
    normalized_name = (name or "").strip().lower()
    normalized_professor = (professor or "").strip().lower()
    for subject in subjects:
        if ignore_id is not None and subject.get("id") == ignore_id:
            continue
        same_name = (subject.get("name") or "").strip().lower() == normalized_name
        same_professor = (subject.get("professor") or "").strip().lower() == normalized_professor
        if same_name and same_professor and not subject_is_archived(subject):
            return True
    return False


def create_subject(payload):
    members_payload = {
        "name": payload.get("name"),
        "code": payload.get("code") or build_subject_code(payload.get("name")),
        "description": payload.get("description"),
        "professor": payload.get("professor"),
        "workload_hours": payload.get("workload_hours"),
        "semester": payload.get("semester"),
    }
    return api_request("POST", "subjects", members_payload)


def update_task(task_id, payload):
    return api_request("PUT", f"tasks/{task_id}", payload)


def update_subject(subject_id, payload):
    patch_payload = {
        "name": payload.get("name"),
        "code": payload.get("code") or build_subject_code(payload.get("name"), subject_id),
        "professor": payload.get("professor"),
        "workload_hours": payload.get("workload_hours"),
        "semester": payload.get("semester"),
        "description": payload.get("description"),
    }
    if "archived" in payload:
        patch_payload["archived"] = bool(payload.get("archived"))
    return api_request("PATCH", f"subjects/{subject_id}", patch_payload)


def delete_subject(subject_id):
    return api_request("DELETE", f"subjects/{subject_id}")


def require_backend_config():
    if get_base_url("auth/login"):
        return True
    st.info("Configure XANO_AUTH_BASE_URL em .streamlit/secrets.toml.")
    return False


def render_auth():
    st.markdown('<div class="auth-shell">', unsafe_allow_html=True)
    st.title("EduTrack AI")
    st.caption("Organize disciplinas, tarefas e progresso acadêmico em um só lugar.")

    tabs = st.tabs(["Entrar", "Criar conta"])
    with tabs[0]:
        with st.form("login_form"):
            email = st.text_input("E-mail")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Entrar", width="stretch")
        if submitted:
            try:
                data = api_request("POST", "auth/login", {"email": email, "password": password})
                st.session_state.auth_token = data.get("authToken")
                st.session_state.auth_expires_at = time.time() + 86400
                fetch_current_user()
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

        with st.expander("Redefinir senha"):
            with st.form("reset_request_form"):
                reset_email = st.text_input("E-mail da conta", key="reset_email")
                reset_submitted = st.form_submit_button("Enviar link de redefinicao", width="stretch")
            if reset_submitted:
                try:
                    data = api_request("GET", "reset/request-reset-link", params={"email": reset_email})
                    st.success("Link de redefinicao enviado para o e-mail informado.")
                    reset_link = ((data or {}).get("message") or {}).get("reset_link") if isinstance(data, dict) else None
                    if reset_link:
                        st.info("Ambiente de teste: use o link abaixo para redefinir a senha.")
                        st.code(reset_link, language=None)
                except Exception as exc:
                    st.error(str(exc))

    with tabs[1]:
        with st.form("signup_form"):
            name = st.text_input("Nome")
            email = st.text_input("E-mail", key="signup_email")
            password = st.text_input("Senha", type="password", key="signup_password")
            submitted = st.form_submit_button("Criar conta", width="stretch")
        if submitted:
            try:
                data = api_request("POST", "auth/signup", {"name": name, "email": email, "password": password})
                st.session_state.auth_token = data.get("authToken")
                st.session_state.auth_expires_at = time.time() + 86400
                fetch_current_user()
                st.rerun()
            except Exception as exc:
                st.error(str(exc))
    st.markdown("</div>", unsafe_allow_html=True)


def render_dashboard(subjects, tasks):
    active_subjects = [subject for subject in subjects if not subject_is_archived(subject)]
    pending_tasks = [task for task in tasks if task.get("status") != "completed"]
    overdue_tasks = [task for task in tasks if is_overdue(task)]
    progress = task_progress(tasks)

    st.header("Dashboard")
    if not subjects and not tasks:
        st.info("Bem-vindo! Cadastre sua primeira disciplina para começar a acompanhar sua rotina acadêmica.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Disciplinas ativas", len(active_subjects))
    col2.metric("Tarefas pendentes", len(pending_tasks))
    col3.metric("Tarefas em atraso", len(overdue_tasks))
    col4.metric("Progresso geral", f"{progress}%")
    st.progress(progress / 100)

    st.subheader("Próximas tarefas")
    upcoming = sorted(pending_tasks, key=lambda task: task.get("due_date") or "")[:5]
    if not upcoming:
        st.success("Nenhuma tarefa pendente no momento.")
    for task in upcoming:
        badge = "ATRASADA" if is_overdue(task) else STATUS_LABELS.get(task.get("status"), task.get("status"))
        st.write(f"**{task.get('title')}** · {task.get('due_date')} · {badge}")


def render_subjects(subjects, tasks):
    st.header("Disciplinas")
    with st.form("subject_form"):
        st.subheader("Nova disciplina")
        col1, col2 = st.columns(2)
        name = col1.text_input("Nome")
        professor = col2.text_input("Professor")
        col3, col4 = st.columns(2)
        workload = col3.number_input("Carga horária", min_value=1, value=40)
        semester = col4.text_input("Semestre/período")
        description = st.text_area("Descrição")
        submitted = st.form_submit_button("Salvar disciplina")
    if submitted:
        try:
            if not name.strip():
                raise RuntimeError("Informe o nome da disciplina.")
            if has_duplicate_subject(subjects, name, professor):
                raise RuntimeError("Já existe uma disciplina ativa com este nome e professor.")
            create_subject({
                "name": name,
                "professor": professor,
                "workload_hours": workload,
                "semester": semester,
                "description": description,
            })
            st.success("Disciplina cadastrada.")
            st.rerun()
        except Exception as exc:
            st.error(str(exc))
    search_col, filter_col, archive_col = st.columns(3)
    search = search_col.text_input("Buscar por nome")
    only_overdue = filter_col.toggle("Com tarefas em atraso", value=False)
    show_archived = archive_col.toggle("Mostrar arquivadas", value=False)
    visible = [subject for subject in subjects if show_archived or not subject_is_archived(subject)]
    if search:
        visible = [subject for subject in visible if search.lower() in subject.get("name", "").lower()]
    if only_overdue:
        visible = [subject for subject in visible if overdue_task_count_for_subject(subject.get("id"), tasks) > 0]

    if not visible:
        st.info("Nenhuma disciplina encontrada para os filtros selecionados.")
        return

    for subject in visible:
        subject_tasks = tasks_for_subject(subject.get("id"), tasks)
        progress = task_progress(subject_tasks)
        overdue_count = overdue_task_count_for_subject(subject.get("id"), tasks)
        with st.expander(subject.get("name", "Disciplina"), expanded=False):
            st.write(f"Professor: {subject.get('professor', '-')}")
            st.write(f"Carga horária: {subject.get('workload_hours') or subject.get('credits') or '-'}")
            st.write(f"Semestre/período: {subject.get('semester', '-')}")
            st.write(f"Progresso: {progress}%")
            st.progress(progress / 100)
            if overdue_count:
                st.error(f"{overdue_count} tarefa(s) em atraso")
            with st.form(f"edit_subject_{subject.get('id')}"):
                name = st.text_input("Nome", value=subject.get("name") or "")
                professor = st.text_input("Professor", value=subject.get("professor") or "")
                workload = st.number_input("Carga horária", min_value=1, value=int(subject.get("workload_hours") or subject.get("credits") or 1))
                semester = st.text_input("Semestre/período", value=subject.get("semester") or "")
                archived = st.checkbox("Arquivada", value=subject_is_archived(subject))
                save = st.form_submit_button("Atualizar")
            if save:
                try:
                    if not name.strip():
                        raise RuntimeError("Informe o nome da disciplina.")
                    if has_duplicate_subject(subjects, name, professor, ignore_id=subject.get("id")):
                        raise RuntimeError("Já existe uma disciplina ativa com este nome e professor.")
                    update_subject(subject.get("id"), {
                        "name": name,
                        "professor": professor,
                        "workload_hours": workload,
                        "semester": semester,
                        "archived": archived,
                    })
                    st.success("Disciplina atualizada.")
                    st.rerun()
                except Exception as exc:
                    st.error(str(exc))

            confirm = st.checkbox("Confirmar exclusão desta disciplina", key=f"confirm_subject_{subject.get('id')}")
            if st.button("Excluir disciplina", key=f"delete_subject_{subject.get('id')}", disabled=not confirm):
                try:
                    delete_subject(subject.get("id"))
                    st.success("Disciplina excluída.")
                    st.rerun()
                except Exception as exc:
                    st.error(str(exc))


def render_tasks(subjects, tasks):
    st.header("Tarefas")
    if not get_base_url("tasks"):
        st.warning("Configure XANO_TASKS_BASE_URL para ativar cadastro, listagem e edição de tarefas.")
    subject_names = {subject.get("id"): subject.get("name") for subject in subjects}
    active_subjects = [subject for subject in subjects if not subject_is_archived(subject)]
    subject_options = {subject.get("name"): subject.get("id") for subject in active_subjects}

    with st.form("task_form"):
        st.subheader("Nova tarefa")
        selected_subject = st.selectbox("Disciplina", list(subject_options.keys()) or ["Cadastre uma disciplina primeiro"])
        title = st.text_input("Título")
        description = st.text_area("Descrição")
        due = st.date_input("Prazo")
        priority_label = st.selectbox("Prioridade", list(PRIORITY_VALUES.keys()), index=1)
        submitted = st.form_submit_button("Salvar tarefa", disabled=not subject_options)
    if submitted:
        try:
            if not title.strip():
                raise RuntimeError("Informe o título da tarefa.")
            api_request("POST", "tasks", {
                "subject_id": subject_options[selected_subject],
                "title": title,
                "description": description,
                "due_date": due.isoformat(),
                "priority": PRIORITY_VALUES[priority_label],
            })
            st.success("Tarefa cadastrada.")
            st.rerun()
        except Exception as exc:
            st.error(str(exc))

    st.subheader("Minhas tarefas")
    filter_col, group_col = st.columns(2)
    status_filter_label = filter_col.selectbox("Status", ["Todos", *STATUS_VALUES.keys()])
    group_by = group_col.radio("Agrupar por", ["Disciplina", "Prazo"], horizontal=True)

    visible_tasks = list(tasks)
    if status_filter_label != "Todos":
        visible_tasks = [task for task in visible_tasks if task.get("status") == STATUS_VALUES[status_filter_label]]

    visible_tasks = sorted(
        visible_tasks,
        key=lambda task: (
            parse_due(task.get("due_date")) or date.max,
            subject_names.get(task.get("subject_id"), ""),
            task.get("title") or "",
        ),
    )

    if not visible_tasks:
        st.info("Nenhuma tarefa encontrada para o filtro selecionado.")
        return

    grouped_tasks = {}
    for task in visible_tasks:
        if group_by == "Disciplina":
            group_name = subject_names.get(task.get("subject_id"), "Sem disciplina")
        else:
            group_name = due_group_label(task)
        grouped_tasks.setdefault(group_name, []).append(task)

    for group_name, group_tasks in grouped_tasks.items():
        st.markdown(f"### {group_name}")
        for task in group_tasks:
            render_task_item(task, subject_options, subject_names)


def render_task_item(task, subject_options, subject_names):
    task_id = task.get("id")
    title = task.get("title", "Tarefa")
    status = task.get("status", "pending")
    status_label = STATUS_LABELS.get(status, status)
    due_date = parse_due(task.get("due_date"))
    overdue_label = " · VENCIDA" if is_overdue(task) else ""
    label = f"{title} · {subject_names.get(task.get('subject_id'), 'Sem disciplina')} · {status_label}{overdue_label}"

    with st.expander(label):
        if is_overdue(task):
            st.error("Prazo vencido")

        st.write(f"Status: {status_label}")
        st.write(f"Prioridade: {PRIORITY_LABELS.get(task.get('priority'), task.get('priority'))}")
        st.write(f"Prazo: {due_date.strftime('%d/%m/%Y') if due_date else '-'}")
        if task.get("description"):
            st.write(task.get("description"))

        current_subject_name = next(
            (name for name, subject_id in subject_options.items() if subject_id == task.get("subject_id")),
            next(iter(subject_options), ""),
        )

        with st.form(f"edit_task_{task_id}"):
            selected_subject = st.selectbox(
                "Disciplina",
                list(subject_options.keys()) or ["Cadastre uma disciplina primeiro"],
                index=list(subject_options.keys()).index(current_subject_name) if current_subject_name in subject_options else 0,
                disabled=not subject_options,
            )
            edit_title = st.text_input("Título", value=task.get("title") or "")
            edit_description = st.text_area("Descrição", value=task.get("description") or "")
            edit_due = st.date_input("Prazo", value=due_date or date.today())
            edit_status_label = st.selectbox(
                "Status",
                list(STATUS_VALUES.keys()),
                index=list(STATUS_VALUES.values()).index(status) if status in STATUS_VALUES.values() else 0,
            )
            edit_priority_label = st.selectbox(
                "Prioridade",
                list(PRIORITY_VALUES.keys()),
                index=list(PRIORITY_VALUES.values()).index(task.get("priority")) if task.get("priority") in PRIORITY_VALUES.values() else 1,
            )
            save_task = st.form_submit_button("Atualizar tarefa", disabled=not subject_options)

        if save_task:
            try:
                if not edit_title.strip():
                    raise RuntimeError("Informe o título da tarefa.")
                update_task(task_id, {
                    "subject_id": subject_options[selected_subject],
                    "title": edit_title,
                    "description": edit_description,
                    "due_date": edit_due.isoformat(),
                    "status": STATUS_VALUES[edit_status_label],
                    "priority": PRIORITY_VALUES[edit_priority_label],
                })
                st.success("Tarefa atualizada.")
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

        action_col, delete_col = st.columns(2)
        if action_col.button("Marcar como concluída", key=f"complete_{task_id}", disabled=status == "completed"):
            try:
                api_request("PATCH", f"tasks/{task_id}/complete")
                st.success("Tarefa concluída.")
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

        confirm = delete_col.checkbox("Confirmar exclusão", key=f"confirm_task_{task_id}")
        if delete_col.button("Excluir tarefa", key=f"delete_task_{task_id}", disabled=not confirm):
            try:
                api_request("DELETE", f"tasks/{task_id}")
                st.success("Tarefa excluída.")
                st.rerun()
            except Exception as exc:
                st.error(str(exc))


def render_reports(subjects, tasks):
    st.header("Relatórios")
    if not get_base_url("tasks"):
        st.info("Relatórios de tarefas ficam completos após configurar XANO_TASKS_BASE_URL.")
    start, end = st.columns(2)
    start_date = start.date_input("Início", value=date(date.today().year, 1, 1))
    end_date = end.date_input("Fim", value=date.today())
    filtered = [task for task in tasks if (parse_due(task.get("due_date")) or date.min) >= start_date and (parse_due(task.get("due_date")) or date.max) <= end_date]

    subject_names = {subject.get("id"): subject.get("name") for subject in subjects}
    rows = []
    for subject in subjects:
        subject_tasks = [task for task in tasks if task.get("subject_id") == subject.get("id")]
        overdue_count = overdue_task_count_for_subject(subject.get("id"), tasks)
        rows.append({
            "Disciplina": subject.get("name"),
            "Semestre": subject.get("semester") or "-",
            "Progresso": f"{task_progress(subject_tasks)}%",
            "Tarefas": len(subject_tasks),
            "Em atraso": overdue_count,
        })
    st.dataframe(rows, width="stretch")

    task_history = [
        {
            "Disciplina": subject_names.get(task.get("subject_id"), "-"),
            "Tarefa": task.get("title"),
            "Status": STATUS_LABELS.get(task.get("status"), task.get("status")),
            "Prioridade": PRIORITY_LABELS.get(task.get("priority"), task.get("priority")),
            "Prazo": task.get("due_date"),
            "Vencida": "Sim" if is_overdue(task) else "Não",
        }
        for task in filtered
    ]
    st.subheader("Histórico de tarefas no período")
    st.dataframe(task_history, width="stretch")

    export_rows = [
        {
            "tipo": "disciplina",
            "disciplina": subject.get("name"),
            "titulo": "",
            "status": "arquivada" if subject_is_archived(subject) else "ativa",
            "prioridade": "",
            "prazo": "",
            "semestre": subject.get("semester") or "",
            "professor": subject.get("professor") or "",
            "progresso": f"{task_progress(tasks_for_subject(subject.get('id'), tasks))}%",
        }
        for subject in subjects
    ] + [
        {
            "tipo": "tarefa",
            "disciplina": subject_names.get(task.get("subject_id")),
            "titulo": task.get("title"),
            "status": task.get("status"),
            "prioridade": task.get("priority"),
            "prazo": task.get("due_date"),
            "semestre": "",
            "professor": "",
            "progresso": "",
        }
        for task in filtered
    ]
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=["tipo", "disciplina", "titulo", "status", "prioridade", "prazo", "semestre", "professor", "progresso"])
    writer.writeheader()
    writer.writerows(export_rows)
    st.download_button("Exportar CSV", csv_buffer.getvalue(), "edutrack-dados.csv", "text/csv")

    pdf_rows = [
        ("Periodo", f"{start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}"),
        ("Disciplinas", str(len(subjects))),
        ("Tarefas no periodo", str(len(filtered))),
    ]
    for subject in subjects:
        subject_tasks = [task for task in tasks if task.get("subject_id") == subject.get("id")]
        completed = [task for task in subject_tasks if task.get("status") == "completed"]
        progress = round((len(completed) / len(subject_tasks)) * 100) if subject_tasks else 0
        pdf_rows.append((f"Disciplina: {subject.get('name', '-')}", f"{progress}% concluido, {len(subject_tasks)} tarefa(s)"))
    for task in filtered:
        pdf_rows.append((f"Tarefa: {task.get('title', '-')}", f"{subject_names.get(task.get('subject_id'), '-')}, {task.get('status', '-')}, {task.get('due_date', '-')}"))

    st.download_button(
        "Exportar PDF",
        generate_pdf_report("Relatorio EduTrack AI", pdf_rows),
        "edutrack-relatorio.pdf",
        "application/pdf",
    )


def escape_pdf_text(value):
    return str(value).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def generate_pdf_report(title, rows):
    lines = [title, ""]
    lines.extend(f"{label}: {value}" for label, value in rows)
    text_commands = ["BT", "/F1 16 Tf", "50 790 Td", f"({escape_pdf_text(lines[0])}) Tj", "/F1 10 Tf"]
    for line in lines[1:]:
        text_commands.append("0 -16 Td")
        text_commands.append(f"({escape_pdf_text(line)}) Tj")
    text_commands.append("ET")
    stream = "\n".join(text_commands).encode("latin-1", errors="replace")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")
    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF".encode("ascii"))
    return bytes(pdf)


def render_profile():
    st.header("Perfil")
    user = st.session_state.get("user") or {}
    with st.form("profile_form"):
        name = st.text_input("Nome", value=user.get("name") or "")
        email = st.text_input("E-mail", value=user.get("email") or "")
        submitted = st.form_submit_button("Salvar perfil")
    if submitted:
        try:
            updated_user = normalize_user(api_request("PATCH", "user/edit_profile", {"name": name, "email": email}))
            st.session_state.user = {**user, **updated_user}
            st.success("Perfil atualizado.")
            st.rerun()
        except Exception as exc:
            st.error(str(exc))

    st.subheader("Senha")
    with st.form("profile_reset_form"):
        reset_email = st.text_input("E-mail para redefinicao", value=email, key="profile_reset_email")
        reset_submitted = st.form_submit_button("Enviar link de redefinicao")
    if reset_submitted:
        try:
            data = api_request("GET", "reset/request-reset-link", params={"email": reset_email})
            st.success("Link de redefinicao enviado para o e-mail informado.")
            reset_link = ((data or {}).get("message") or {}).get("reset_link") if isinstance(data, dict) else None
            if reset_link:
                st.info("Ambiente de teste: use o link abaixo para redefinir a senha.")
                st.code(reset_link, language=None)
        except Exception as exc:
            st.error(str(exc))
    return


def apply_theme():
    st.markdown(
        """
        <style>
        .stApp { background: #f7f9fc; color: #172033; }
        h1, h2, h3 { color: #16243a; letter-spacing: 0; }
        section[data-testid="stSidebar"] { background: #132238; }
        section[data-testid="stSidebar"] * { color: #f8fbff; }
        div[data-testid="stMetric"] {
          background: #ffffff;
          border: 1px solid #d9e2ef;
          border-radius: 8px;
          padding: 14px;
        }
        .stTextInput, .stTextArea, .stSelectbox, .stNumberInput, .stDateInput, .stToggle, .stFileUploader {
          color: #172033;
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input, .stDateInput input {
          background: #ffffff !important;
          color: #172033 !important;
        }
        .stTextInput, .stTextArea, .stSelectbox, .stNumberInput, .stDateInput {
          border-color: #d9e2ef !important;
        }
        button, input[type="submit"], input[type="button"], .stButton>button {
          background-color: #2f6fe8 !important;
          color: #ffffff !important;
          border: none !important;
        }
        .stButton>button:hover, button:hover, input[type="submit"]:hover, input[type="button"]:hover {
          background-color: #245bcc !important;
        }
        [role="tab"] {
          background: #ffffff !important;
          color: #172033 !important;
          border: 1px solid #d9e2ef !important;
        }
        [role="tab"][aria-selected="true"] {
          background: #2f6fe8 !important;
          color: #ffffff !important;
          border-color: #2f6fe8 !important;
        }
        .auth-shell {
          max-width: 760px;
          margin: 40px auto;
          padding: 24px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    init_state()
    apply_theme()

    if not require_backend_config():
        return

    if not is_authenticated():
        render_auth()
        return

    if st.session_state.get("user") is None:
        fetch_current_user()

    st.sidebar.title("EduTrack AI")
    page = st.sidebar.radio("Navegar", ["Dashboard", "Disciplinas", "Tarefas", "Relatórios", "Perfil"])
    if st.sidebar.button("Sair"):
        logout()
        st.rerun()

    try:
        subjects = fetch_subjects(include_archived=True)
        tasks = fetch_tasks()
    except Exception as exc:
        st.error(str(exc))
        return

    if page == "Dashboard":
        render_dashboard(subjects, tasks)
    elif page == "Disciplinas":
        render_subjects(subjects, tasks)
    elif page == "Tarefas":
        render_tasks(subjects, tasks)
    elif page == "Relatórios":
        render_reports(subjects, tasks)
    else:
        render_profile()


if __name__ == "__main__":
    main()
