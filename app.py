import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import datetime
from database import (init_db, create_connection, add_client, get_all_clients, get_client_by_id, update_client, delete_client, search_clients,
                   check_client_exists, add_service, get_all_services, get_service_by_id, update_service, delete_service, search_services,
                   get_services_by_category, get_service_categories, get_service_statistics, add_appointment, get_all_appointments, update_appointment, delete_appointment, 
                   get_appointments_by_date, get_appointment_by_id, get_appointments_by_client, get_pending_appointments_with_clients,
                   get_appointment_statistics, mark_appointment_as_completed, save_invoice)

# Initialize the database
init_db()

# Set page configuration
st.set_page_config(
    page_title="Lucero Glam Studio",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #FF69B4;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .subheader {
        font-size: 1.5rem;
        color: #FF69B4;
        margin-bottom: 1rem;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .success-message {
        color: #28a745;
        padding: 0.5rem;
        border-radius: 0.3rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .error-message {
        color: #721c24;
        padding: 0.5rem;
        border-radius: 0.3rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    .info-message {
        color: #0c5460;
        padding: 0.5rem;
        border-radius: 0.3rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Main header
st.markdown("<h1 class='main-header'>Lucero Glam Studio</h1>", unsafe_allow_html=True)

# Sidebar for navigation and management
with st.sidebar:
    st.markdown("<h2 class='subheader'>Lucero Glam Studio</h2>", unsafe_allow_html=True)
    
    # Create tabs for different sections
    section = st.selectbox("Seleccione una sección:", ["Clientes", "Servicios", "Citas", "Facturación"])
    
    # Importamos os para manejar archivos
    import os
    
    if section == "Clientes":
        st.markdown("<h3 class='subheader'>Gestión de Clientes</h3>", unsafe_allow_html=True)
        
        # Create tabs for different client operations
        client_tab = st.radio("Seleccione una opción:", ["Registrar Cliente", "Buscar y Editar Clientes"])
        
        if client_tab == "Registrar Cliente":
            st.markdown("<h4>Registrar Nuevo Cliente</h4>", unsafe_allow_html=True)
            
            # Client registration form
            with st.form(key="client_registration_form"):
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("Nombre*")
                with col2:
                    last_name = st.text_input("Apellido*")
                
                phone_number = st.text_input("Número de Teléfono*")
                description = st.text_area("Descripción (Opcional)")
                
                submit_button = st.form_submit_button(label="Registrar Cliente")
                
                if submit_button:
                    if not first_name or not last_name or not phone_number:
                        st.markdown("<div class='error-message'>Por favor complete todos los campos obligatorios.</div>", unsafe_allow_html=True)
                    else:
                        # Verificar si el cliente ya existe
                        if check_client_exists(first_name, last_name, phone_number):
                            st.markdown("<div class='error-message'>Lo siento, el cliente que desea crear ya está creado. Si desea puede editarlo en el apartado de editar o eliminar.</div>", unsafe_allow_html=True)
                        else:
                            # Add client to database
                            client_id = add_client(first_name, last_name, phone_number, description)
                            if client_id:
                                st.markdown("<div class='success-message'>¡El Cliente se ha creado exitosamente!</div>", unsafe_allow_html=True)
                                # Clear form fields after successful submission
                                st.rerun()
                            else:
                                st.markdown("<div class='error-message'>Error al registrar el cliente. Intente nuevamente.</div>", unsafe_allow_html=True)
        
        elif client_tab == "Buscar y Editar Clientes":
            st.markdown("<h4>Buscar Clientes</h4>", unsafe_allow_html=True)
            search_term = st.text_input("Buscar por nombre o teléfono")
            
            if search_term:
                clients = search_clients(search_term)
            else:
                clients = get_all_clients()
            
            if clients:
                # Convert to DataFrame for better display
                df = pd.DataFrame(clients, columns=["ID", "Nombre", "Apellido", "Teléfono", "Descripción", "Fecha de Registro"])
                
                # Display clients in a table
                st.dataframe(df[["ID", "Nombre", "Apellido", "Teléfono"]], use_container_width=True)
                
                # Select client to edit
                selected_client_id = st.selectbox("Seleccionar cliente para editar/eliminar:", 
                                                options=[client[0] for client in clients],
                                                format_func=lambda x: f"{dict(zip(df['ID'], df['Nombre'] + ' ' + df['Apellido']))[x]}")
                
                if selected_client_id:
                    client = get_client_by_id(selected_client_id)
                    if client:
                        with st.form(key="edit_client_form"):
                            st.markdown("<h4>Editar Cliente</h4>", unsafe_allow_html=True)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                edit_first_name = st.text_input("Nombre*", value=client[1])
                            with col2:
                                edit_last_name = st.text_input("Apellido*", value=client[2])
                            
                            edit_phone_number = st.text_input("Número de Teléfono*", value=client[3])
                            edit_description = st.text_area("Descripción (Opcional)", value=client[4] if client[4] else "")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                update_button = st.form_submit_button(label="Actualizar Cliente")
                            with col2:
                                delete_button = st.form_submit_button(label="Eliminar Cliente", type="primary")
                            
                            if update_button:
                                if not edit_first_name or not edit_last_name or not edit_phone_number:
                                    st.markdown("<div class='error-message'>Por favor complete todos los campos obligatorios.</div>", unsafe_allow_html=True)
                                else:
                                    # Update client in database
                                    rows_affected = update_client(selected_client_id, edit_first_name, edit_last_name, edit_phone_number, edit_description)
                                    if rows_affected > 0:
                                        st.markdown("<div class='success-message'>¡El cliente se editó correctamente!</div>", unsafe_allow_html=True)
                                        st.rerun()
                                    else:
                                        st.markdown("<div class='error-message'>Error al actualizar el cliente. Intente nuevamente.</div>", unsafe_allow_html=True)
                            
                            if delete_button:
                                # Delete client from database
                                rows_affected = delete_client(selected_client_id)
                                if rows_affected > 0:
                                    st.markdown("<div class='success-message'>¡El cliente se ha eliminado correctamente!</div>", unsafe_allow_html=True)
                                    st.rerun()
                                else:
                                    st.markdown("<div class='error-message'>Error al eliminar el cliente. Intente nuevamente.</div>", unsafe_allow_html=True)
            else:
                st.info("No se encontraron clientes.")
    
    elif section == "Servicios":
        st.markdown("<h3 class='subheader'>Gestión de Servicios</h3>", unsafe_allow_html=True)
        
        # Create tabs for different service operations
        service_tab = st.radio("Seleccione una opción:", ["Registrar Servicio", "Buscar y Editar Servicios", "Estadísticas de Servicios"])
        
        if service_tab == "Registrar Servicio":
            st.markdown("<h4>Registrar Nuevo Servicio</h4>", unsafe_allow_html=True)
            
            # Service registration form
            with st.form(key="service_registration_form"):
                service_name = st.text_input("Nombre del Servicio*")
                
                col1, col2 = st.columns(2)
                with col1:
                    service_price = st.number_input("Precio*", min_value=0.0, step=0.01, format="%.2f")
                with col2:
                    service_duration = st.number_input("Duración (minutos)*", min_value=5, step=5)
                
                # Opciones predefinidas de categorías + opción para crear nueva
                default_categories = ["General", "Maquillaje", "Peinado", "Uñas", "Tratamientos", "Otro"]
                service_category = st.selectbox(
                    "Categoría*",
                    options=default_categories,
                    index=0
                )
                
                # Si selecciona "Otro", mostrar campo para ingresar nueva categoría
                if service_category == "Otro":
                    new_category = st.text_input("Especifique la nueva categoría")
                    if new_category:
                        service_category = new_category
                
                service_description = st.text_area("Descripción (Opcional)")
                
                submit_service_button = st.form_submit_button(label="Registrar Servicio")
                
                if submit_service_button:
                    if not service_name or service_price <= 0 or service_duration <= 0:
                        st.markdown("<div class='error-message'>Por favor complete todos los campos obligatorios.</div>", unsafe_allow_html=True)
                    else:
                        # Add service to database
                        service_id = add_service(service_name, service_price, service_duration, service_description, service_category)
                        if service_id:
                            st.markdown("<div class='success-message'>¡Servicio registrado exitosamente!</div>", unsafe_allow_html=True)
                            # Clear form fields after successful submission
                            st.rerun()
                        else:
                            st.markdown("<div class='error-message'>Error al registrar el servicio. Intente nuevamente.</div>", unsafe_allow_html=True)
        
        elif service_tab == "Buscar y Editar Servicios":
            st.markdown("<h4>Buscar Servicios</h4>", unsafe_allow_html=True)
            
            # Opciones de filtrado
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Obtener todas las categorías existentes
                categories = ["Todas"] + get_service_categories()
                filter_category = st.selectbox("Filtrar por categoría", options=categories, index=0)
            
            with col2:
                search_term = st.text_input("Buscar por nombre")
            
            # Aplicar filtros
            if search_term:
                services = search_services(search_term)
            elif filter_category != "Todas":
                services = get_services_by_category(filter_category)
            else:
                services = get_all_services()
            
            if services:
                # Convert to DataFrame for better display
                df = pd.DataFrame(services, columns=["ID", "Nombre", "Precio", "Duración (min)", "Descripción", "Categoría"])
                
                # Format price column
                df["Precio"] = df["Precio"].apply(lambda x: f"${x:.2f}")
                
                # Display services in a table
                st.dataframe(df[["ID", "Nombre", "Precio", "Duración (min)", "Categoría"]], use_container_width=True)
                
                # Select service to edit
                selected_service_id = st.selectbox("Seleccionar servicio para editar/eliminar:", 
                                                 options=[service[0] for service in services],
                                                 format_func=lambda x: f"{dict(zip(df['ID'], df['Nombre']))[x]}")
                
                if selected_service_id:
                    service = get_service_by_id(selected_service_id)
                    if service:
                        with st.form(key="edit_service_form"):
                            st.markdown("<h4>Editar Servicio</h4>", unsafe_allow_html=True)
                            
                            edit_service_name = st.text_input("Nombre del Servicio*", value=service[1])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                edit_service_price = st.number_input("Precio*", min_value=0.0, step=0.01, format="%.2f", value=float(service[2]))
                            with col2:
                                edit_service_duration = st.number_input("Duración (minutos)*", min_value=5, step=5, value=int(service[3]))
                            
                            # Obtener la categoría actual del servicio (índice 5 si existe, sino usar "General")
                            current_category = service[5] if len(service) > 5 else "General"
                            
                            # Opciones predefinidas de categorías + opción para crear nueva
                            default_categories = ["General", "Maquillaje", "Peinado", "Uñas", "Tratamientos", "Otro"]
                            # Asegurar que la categoría actual esté en la lista
                            if current_category not in default_categories:
                                default_categories.append(current_category)
                                
                            edit_service_category = st.selectbox(
                                "Categoría*",
                                options=default_categories,
                                index=default_categories.index(current_category)
                            )
                            
                            # Si selecciona "Otro", mostrar campo para ingresar nueva categoría
                            if edit_service_category == "Otro":
                                new_category = st.text_input("Especifique la nueva categoría")
                                if new_category:
                                    edit_service_category = new_category
                            
                            edit_service_description = st.text_area("Descripción (Opcional)", value=service[4] if service[4] else "")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                update_service_button = st.form_submit_button(label="Actualizar Servicio")
                            with col2:
                                delete_service_button = st.form_submit_button(label="Eliminar Servicio", type="primary")
                            
                            if update_service_button:
                                if not edit_service_name or edit_service_price <= 0 or edit_service_duration <= 0:
                                    st.markdown("<div class='error-message'>Por favor complete todos los campos obligatorios.</div>", unsafe_allow_html=True)
                                else:
                                    # Update service in database
                                    rows_affected = update_service(selected_service_id, edit_service_name, edit_service_price, edit_service_duration, edit_service_description, edit_service_category)
                                    if rows_affected > 0:
                                        st.markdown("<div class='success-message'>¡El servicio se actualizó correctamente!</div>", unsafe_allow_html=True)
                                        st.rerun()
                                    else:
                                        st.markdown("<div class='error-message'>Error al actualizar el servicio. Intente nuevamente.</div>", unsafe_allow_html=True)
                            
                            if delete_service_button:
                                # Delete service from database
                                rows_affected = delete_service(selected_service_id)
                                if rows_affected > 0:
                                    st.markdown("<div class='success-message'>¡El servicio se ha eliminado correctamente!</div>", unsafe_allow_html=True)
                                    st.rerun()
                                else:
                                    st.markdown("<div class='error-message'>Error al eliminar el servicio. Intente nuevamente.</div>", unsafe_allow_html=True)
            else:
                st.info("No se encontraron servicios.")
                
        elif service_tab == "Estadísticas de Servicios":
            st.markdown("<h4>Estadísticas de Servicios</h4>", unsafe_allow_html=True)
            
            # Obtener estadísticas de servicios
            stats = get_service_statistics()
            
            if stats and stats.get('total_services', 0) > 0:
                # Crear layout con columnas para métricas
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total de Servicios", stats['total_services'])
                
                with col2:
                    avg_price = stats.get('avg_price', 0)
                    st.metric("Precio Promedio", f"${avg_price:.2f}")
                
                with col3:
                    most_common_duration = stats.get('most_common_duration')
                    if most_common_duration:
                        st.metric("Duración más común", f"{most_common_duration[0]} min")
                
                # Información sobre servicio más caro
                st.subheader("Servicio más costoso")
                most_expensive = stats.get('most_expensive')
                if most_expensive:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"**{most_expensive[0]}**\n\nPrecio: ${most_expensive[1]:.2f}\n\nCategoría: {most_expensive[2]}")
                
                # Gráfico de servicios por categoría
                st.subheader("Servicios por Categoría")
                services_by_category = stats.get('services_by_category', [])
                
                if services_by_category:
                    # Preparar datos para el gráfico
                    categories = [cat[0] for cat in services_by_category]
                    counts = [cat[1] for cat in services_by_category]
                    
                    # Crear gráfico de barras
                    import matplotlib.pyplot as plt
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    bars = ax.bar(categories, counts, color='#FF69B4')
                    
                    # Añadir etiquetas y título
                    ax.set_xlabel('Categoría')
                    ax.set_ylabel('Cantidad de Servicios')
                    ax.set_title('Distribución de Servicios por Categoría')
                    
                    # Añadir valores en las barras
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                                f'{height:.0f}', ha='center', va='bottom')
                    
                    # Ajustar diseño
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    
                    # Mostrar gráfico en Streamlit
                    st.pyplot(fig)
                    
                    # Mostrar tabla con datos
                    df_categories = pd.DataFrame(services_by_category, columns=['Categoría', 'Cantidad'])
                    st.dataframe(df_categories, use_container_width=True)
            else:
                st.info("No hay suficientes datos para mostrar estadísticas de servicios.")
    
    elif section == "Citas":
        st.markdown("<h3 class='subheader'>Gestión de Citas</h3>", unsafe_allow_html=True)
        
        # Create tabs for different appointment operations
        appointment_tab = st.radio("Seleccione una opción:", ["Agendar Cita", "Buscar y Editar Citas", "Calendario de Citas", "Estadísticas de Citas"])
        
        if appointment_tab == "Agendar Cita":
            st.markdown("<h4>Agendar Nueva Cita</h4>", unsafe_allow_html=True)
            
            # Get all clients and services for selection
            clients = get_all_clients()
            services = get_all_services()
            
            if not clients:
                st.warning("No hay clientes registrados. Por favor, registre al menos un cliente antes de agendar una cita.")
            elif not services:
                st.warning("No hay servicios registrados. Por favor, registre al menos un servicio antes de agendar una cita.")
            else:
                # Appointment registration form
                with st.form(key="appointment_registration_form"):
                    # Client selection
                    client_options = {client[0]: f"{client[1]} {client[2]}" for client in clients}
                    selected_client_id = st.selectbox("Seleccionar Cliente*", options=list(client_options.keys()), 
                                                    format_func=lambda x: client_options[x])
                    
                    # Service selection
                    service_options = {service[0]: f"{service[1]} - ${service[3]:.2f}" for service in services}
                    selected_service_id = st.selectbox("Seleccionar Servicio*", options=list(service_options.keys()), 
                                                     format_func=lambda x: service_options[x])
                    
                    # Date and time selection
                    col1, col2 = st.columns(2)
                    with col1:
                        appointment_date = st.date_input("Fecha de la Cita*", min_value=datetime.datetime.now().date())
                    with col2:
                        appointment_time = st.time_input("Hora de la Cita*", value=datetime.time(9, 0))
                    
                    # Combine date and time
                    appointment_datetime = datetime.datetime.combine(appointment_date, appointment_time)
                    
                    # Deposit amount
                    deposit_amount = st.number_input("Aparto con ($)*", min_value=0.0, step=10.0, format="%.2f")
                    
                    # Notes
                    notes = st.text_area("Notas Adicionales (Opcional)")
                    
                    submit_appointment_button = st.form_submit_button(label="Agendar Cita")
                    
                    if submit_appointment_button:
                        if deposit_amount <= 0:
                            st.markdown("<div class='error-message'>Por favor ingrese un monto de apartado válido.</div>", unsafe_allow_html=True)
                        else:
                            # Add appointment to database
                            appointment_id = add_appointment(selected_client_id, selected_service_id, appointment_datetime, deposit_amount, notes)
                            
                            if appointment_id == -1:  # Time conflict
                                st.markdown("<div class='error-message'>Lo sentimos señora Lucero, la cita que desea agendar no está disponible porque hay otra cita agendada para esa hora exacta, por favor seleccione otra hora para agendar la cita.</div>", unsafe_allow_html=True)
                            elif appointment_id:
                                st.markdown("<div class='success-message'>¡Cita agendada exitosamente!</div>", unsafe_allow_html=True)
                                # Clear form fields after successful submission
                                st.rerun()
                            else:
                                st.markdown("<div class='error-message'>Error al agendar la cita. Intente nuevamente.</div>", unsafe_allow_html=True)
        
        elif appointment_tab == "Buscar y Editar Citas":
            st.markdown("<h4>Buscar Citas</h4>", unsafe_allow_html=True)
            
            # Get all appointments
            appointments = get_all_appointments()
            
            if appointments:
                # Convert to DataFrame for better display
                df = pd.DataFrame(appointments, columns=["ID", "Nombre", "Apellido", "Servicio", "Fecha y Hora", "Apartado ($)", "Notas", "Estado"])
                
                # Format date and deposit amount
                df["Fecha y Hora"] = pd.to_datetime(df["Fecha y Hora"])
                df["Fecha y Hora"] = df["Fecha y Hora"].dt.strftime("%d/%m/%Y %H:%M")
                df["Apartado ($)"] = df["Apartado ($)"].apply(lambda x: f"${x:.2f}")
                
                # Display appointments in a table
                st.dataframe(df[["ID", "Nombre", "Apellido", "Servicio", "Fecha y Hora", "Apartado ($)", "Estado"]], use_container_width=True)
                
                # Select appointment to edit
                selected_appointment_id = st.selectbox("Seleccionar cita para editar/eliminar:", 
                                                    options=[appointment[0] for appointment in appointments],
                                                    format_func=lambda x: f"ID: {x} - {dict(zip(df['ID'], df['Nombre'] + ' ' + df['Apellido'] + ' - ' + df['Fecha y Hora']))[x]}")
                
                if selected_appointment_id:
                    appointment = get_appointment_by_id(selected_appointment_id)
                    if appointment:
                        # Get all clients and services for selection
                        clients = get_all_clients()
                        services = get_all_services()
                        
                        with st.form(key="edit_appointment_form"):
                            st.markdown("<h4>Editar Cita</h4>", unsafe_allow_html=True)
                            
                            # Client selection
                            client_options = {client[0]: f"{client[1]} {client[2]}" for client in clients}
                            edit_client_id = st.selectbox("Seleccionar Cliente*", options=list(client_options.keys()), 
                                                        index=list(client_options.keys()).index(appointment[1]) if appointment[1] in client_options else 0,
                                                        format_func=lambda x: client_options[x])
                            
                            # Service selection
                            service_options = {service[0]: f"{service[1]} - ${service[3]:.2f}" for service in services}
                            edit_service_id = st.selectbox("Seleccionar Servicio*", options=list(service_options.keys()), 
                                                         index=list(service_options.keys()).index(appointment[2]) if appointment[2] in service_options else 0,
                                                         format_func=lambda x: service_options[x])
                            
                            # Parse existing date and time
                            existing_datetime = datetime.datetime.strptime(appointment[3], "%Y-%m-%d %H:%M")
                            
                            # Date and time selection
                            col1, col2 = st.columns(2)
                            with col1:
                                edit_appointment_date = st.date_input("Fecha de la Cita*", value=existing_datetime.date())
                            with col2:
                                edit_appointment_time = st.time_input("Hora de la Cita*", value=existing_datetime.time())
                            
                            # Combine date and time
                            edit_appointment_datetime = datetime.datetime.combine(edit_appointment_date, edit_appointment_time)
                            
                            # Deposit amount
                            edit_deposit_amount = st.number_input("Aparto con ($)*", min_value=0.0, value=float(appointment[4]), step=10.0, format="%.2f")
                            
                            # Notes
                            edit_notes = st.text_area("Notas Adicionales (Opcional)", value=appointment[5] if appointment[5] else "")
                            
                            # Status - Traducción de opciones a español pero manteniendo valores en inglés para la base de datos
                            status_options = {"scheduled": "Programada", "completed": "Completada", "cancelled": "Cancelada"}
                            status_list = ["scheduled", "completed", "cancelled"]
                            edit_status = st.selectbox("Estado de la Cita", 
                                                      options=status_list, 
                                                      format_func=lambda x: status_options[x],
                                                      index=status_list.index(appointment[6]))
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                update_appointment_button = st.form_submit_button(label="Actualizar Cita")
                            with col2:
                                delete_appointment_button = st.form_submit_button(label="Eliminar Cita", type="primary")
                            
                            if update_appointment_button:
                                if edit_deposit_amount <= 0:
                                    st.markdown("<div class='error-message'>Por favor ingrese un monto de apartado válido.</div>", unsafe_allow_html=True)
                                else:
                                    # Update appointment in database
                                    result = update_appointment(selected_appointment_id, edit_client_id, edit_service_id, 
                                                              edit_appointment_datetime, edit_deposit_amount, edit_notes, edit_status)
                                    
                                    if result == -1:  # Time conflict
                                        st.markdown("<div class='error-message'>Lo sentimos señora Lucero, la cita que desea agendar no está disponible porque hay otra cita agendada para esa hora exacta, por favor seleccione otra hora para agendar la cita.</div>", unsafe_allow_html=True)
                                    elif result > 0:
                                        st.markdown("<div class='success-message'>¡Cita actualizada exitosamente!</div>", unsafe_allow_html=True)
                                        st.rerun()
                                    else:
                                        st.markdown("<div class='error-message'>Error al actualizar la cita. Intente nuevamente.</div>", unsafe_allow_html=True)
                            
                            if delete_appointment_button:
                                # Delete appointment from database
                                rows_affected = delete_appointment(selected_appointment_id)
                                if rows_affected > 0:
                                    st.markdown("<div class='success-message'>¡Cita eliminada exitosamente!</div>", unsafe_allow_html=True)
                                    st.rerun()
                                else:
                                    st.markdown("<div class='error-message'>Error al eliminar la cita. Intente nuevamente.</div>", unsafe_allow_html=True)
            else:
                st.info("No hay citas registradas.")
        
        elif appointment_tab == "Calendario de Citas":
            st.markdown("<h4>Calendario de Citas</h4>", unsafe_allow_html=True)
            
            # Date selection for calendar view
            selected_date = st.date_input("Seleccione una fecha para ver las citas", value=datetime.datetime.now().date())
            
            # Get appointments for the selected date
            appointments = get_appointments_by_date(selected_date)
            
            if appointments:
                st.markdown(f"<h5>Citas para el {selected_date.strftime('%d/%m/%Y')}</h5>", unsafe_allow_html=True)
                
                # Create a visual calendar/timeline
                hours = list(range(8, 21))  # 8 AM to 8 PM
                
                # Create a dictionary to store appointments by hour
                appointments_by_hour = {}
                for hour in hours:
                    appointments_by_hour[hour] = []
                
                # Organize appointments by hour
                for appointment in appointments:
                    appointment_time = datetime.datetime.strptime(appointment[4], "%Y-%m-%d %H:%M")
                    hour = appointment_time.hour
                    if hour in appointments_by_hour:
                        appointments_by_hour[hour].append(appointment)
                
                # Display appointments in a timeline
                for hour in hours:
                    col1, col2 = st.columns([1, 5])
                    with col1:
                        st.write(f"**{hour}:00**")
                    with col2:
                        if appointments_by_hour[hour]:
                            for appointment in appointments_by_hour[hour]:
                                with col2:
                                    # Display appointment details
                                    st.markdown(f"**{appointment[1]} {appointment[2]}** - {appointment[3]}")
                                    st.markdown(f"Hora: {datetime.datetime.strptime(appointment[4], '%Y-%m-%d %H:%M').strftime('%H:%M')} | Duración: {appointment[8]} min")
                                    st.markdown(f"Apartado: ${float(appointment[5]):.2f} | Estado: {appointment[7]}")
                                    st.markdown("---")
                                    box_color = "#F44336"  # Rojo para citas canceladas
                                
                                st.markdown(f"""
                                <div style="padding: 10px; border-radius: 5px; background-color: {box_color}; margin-bottom: 10px;">
                                    <strong>{appointment_time.strftime('%H:%M')} - {client_name}</strong><br>
                                    Servicio: {service_name}<br>
                                    Apartado: ${deposit:.2f}<br>
                                    Estado: {status.replace('scheduled', 'Programada').replace('completed', 'Completada').replace('cancelled', 'Cancelada')}
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.markdown("<div style='padding: 10px; border: 1px dashed #ccc; border-radius: 5px;'>Disponible</div>", unsafe_allow_html=True)
                    st.markdown("<hr style='margin: 5px 0;'>", unsafe_allow_html=True)
            else:
                st.info(f"No hay citas programadas para el {selected_date.strftime('%d/%m/%Y')}.")
                
        elif appointment_tab == "Estadísticas de Citas":
            st.markdown("<h4>Estadísticas de Citas</h4>", unsafe_allow_html=True)
            
            # Obtener estadísticas de citas
            stats = get_appointment_statistics()
            
            if stats and stats.get('total_appointments', 0) > 0:
                # Crear layout con columnas para métricas principales
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total de Citas", stats['total_appointments'])
                
                with col2:
                    upcoming = stats.get('upcoming_appointments_7_days', 0)
                    st.metric("Citas próximos 7 días", upcoming)
                
                with col3:
                    last_month = stats.get('appointments_last_30_days', 0)
                    st.metric("Citas últimos 30 días", last_month)
                
                # Segunda fila de métricas
                col1, col2 = st.columns(2)
                
                with col1:
                    total_revenue = stats.get('total_revenue', 0)
                    st.metric("Ingresos Totales", f"${total_revenue:.2f}")
                
                with col2:
                    avg_deposit = stats.get('avg_deposit', 0)
                    st.metric("Apartado Promedio", f"${avg_deposit:.2f}")
                
                # Información sobre servicio más popular
                st.subheader("Servicio Más Popular")
                most_popular = stats.get('most_popular_service')
                if most_popular:
                    st.info(f"**{most_popular[0]}**\n\nNúmero de citas: {most_popular[1]}")
                
                # Información sobre cliente más activo
                st.subheader("Cliente Más Frecuente")
                most_active = stats.get('most_active_client')
                if most_active:
                    st.info(f"**{most_active[0]}**\n\nNúmero de citas: {most_active[1]}")
                
                # Gráficos
                st.subheader("Distribución de Citas")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Gráfico de citas por estado
                    appointments_by_status = stats.get('appointments_by_status', [])
                    if appointments_by_status:
                        # Traducir estados a español
                        status_mapping = {"scheduled": "Programada", "completed": "Completada", "cancelled": "Cancelada"}
                        labels = [status_mapping.get(status[0], status[0]) for status in appointments_by_status]
                        sizes = [status[1] for status in appointments_by_status]
                        
                        # Crear gráfico circular
                        import matplotlib.pyplot as plt
                        
                        fig1, ax1 = plt.subplots(figsize=(8, 6))
                        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#FF69B4', '#90EE90', '#FFA07A'])
                        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
                        plt.title('Citas por Estado')
                        
                        st.pyplot(fig1)
                
                with col2:
                    # Gráfico de citas por día de la semana
                    appointments_by_day = stats.get('appointments_by_day', [])
                    if appointments_by_day:
                        days = [day[0] for day in appointments_by_day]
                        counts = [day[1] for day in appointments_by_day]
                        
                        # Crear gráfico de barras
                        fig2, ax2 = plt.subplots(figsize=(8, 6))
                        bars = ax2.bar(days, counts, color='#FF69B4')
                        
                        # Añadir etiquetas y título
                        ax2.set_xlabel('Día de la Semana')
                        ax2.set_ylabel('Número de Citas')
                        ax2.set_title('Citas por Día de la Semana')
                        
                        # Añadir valores en las barras
                        for bar in bars:
                            height = bar.get_height()
                            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                                    f'{height:.0f}', ha='center', va='bottom')
                        
                        plt.tight_layout()
                        st.pyplot(fig2)
                
                # Tabla de datos
                st.subheader("Resumen por Estado")
                if appointments_by_status:
                    # Crear DataFrame para mostrar datos
                    status_data = [(status_mapping.get(s[0], s[0]), s[1]) for s in appointments_by_status]
                    df_status = pd.DataFrame(status_data, columns=['Estado', 'Cantidad'])
                    st.dataframe(df_status, use_container_width=True)
            else:
                st.info("No hay suficientes datos para mostrar estadísticas de citas.")
    
    elif section == "Facturación":
        st.markdown("<h3 class='subheader'>Facturación</h3>", unsafe_allow_html=True)
        
        # Inicializar variables de sesión si no existen
        if 'invoice_generated' not in st.session_state:
            st.session_state.invoice_generated = False
            st.session_state.invoice_filename = ""
            st.session_state.invoice_content = ""
            st.session_state.invoice_id = 0
        
        # Obtener todas las citas programadas con información del cliente
        pending_appointments = get_pending_appointments_with_clients()
        
        if not pending_appointments and not st.session_state.invoice_generated:
            st.warning("No hay citas programadas pendientes para facturar.")
        else:
            # Si no se ha generado una factura, mostrar el formulario
            if not st.session_state.invoice_generated:
                # Crear opciones para el selectbox
                appointment_options = {appointment[0]: f"{appointment[2]} {appointment[3]} - {appointment[5]} - {datetime.datetime.strptime(appointment[7], '%Y-%m-%d %H:%M').strftime('%d/%m/%Y %H:%M')}" for appointment in pending_appointments}
                
                # Formulario de facturación
                with st.form(key="invoice_form"):
                    st.markdown("<h4>Facturar Cita</h4>", unsafe_allow_html=True)
                    
                    # Seleccionar cita
                    selected_appointment_id = st.selectbox(
                        "Seleccionar cita del cliente*", 
                        options=list(appointment_options.keys()),
                        format_func=lambda x: appointment_options[x]
                    )
                    
                    # Obtener detalles de la cita seleccionada
                    selected_appointment = next((a for a in pending_appointments if a[0] == selected_appointment_id), None)
                    
                    if selected_appointment:
                        # Mostrar información de la cita
                        service_price = selected_appointment[6]  # Precio del servicio
                        deposit_amount = selected_appointment[8]  # Monto del apartado
                        remaining_amount = service_price - deposit_amount  # Monto restante a pagar
                        
                        st.markdown(f"""
                        <div style='background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin-bottom: 15px;'>
                            <h5>Detalles de la Cita</h5>
                            <p><strong>Cliente:</strong> {selected_appointment[2]} {selected_appointment[3]}</p>
                            <p><strong>Servicio:</strong> {selected_appointment[5]}</p>
                            <p><strong>Fecha y Hora:</strong> {datetime.datetime.strptime(selected_appointment[7], '%Y-%m-%d %H:%M').strftime('%d/%m/%Y %H:%M')}</p>
                            <p><strong>Precio del Servicio:</strong> ${service_price:.2f}</p>
                            <p><strong>Apartado Pagado:</strong> ${deposit_amount:.2f}</p>
                            <p><strong>Monto Restante a Pagar:</strong> ${remaining_amount:.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Campos adicionales para facturación
                        col1, col2 = st.columns(2)
                        with col1:
                            late_fee = st.number_input("Mora (Opcional)", min_value=0.0, value=0.0, step=10.0, format="%.2f")
                        with col2:
                            discount = st.number_input("Descuento (Opcional)", min_value=0.0, value=0.0, step=10.0, format="%.2f")
                        
                        # Calcular total con mora y descuento
                        total_to_pay = remaining_amount + late_fee - discount
                        
                        # Monto con el que paga el cliente
                        payment_amount = st.number_input("Monto con el que paga*", min_value=total_to_pay, value=total_to_pay, step=10.0, format="%.2f")
                        
                        # Calcular cambio
                        change_amount = payment_amount - total_to_pay
                        
                        # Botones para calcular y facturar
                        col1, col2 = st.columns(2)
                        with col1:
                            calculate_button = st.form_submit_button(label="Calcular")
                        with col2:
                            invoice_button = st.form_submit_button(label="Generar Factura")
                    
                    if calculate_button:
                        # Mostrar resumen de la factura
                        st.markdown(f"""
                        <div style='background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 15px;'>
                            <h5>Resumen de Facturación</h5>
                            <p><strong>Monto Restante:</strong> ${remaining_amount:.2f}</p>
                            <p><strong>Mora:</strong> ${late_fee:.2f}</p>
                            <p><strong>Descuento:</strong> ${discount:.2f}</p>
                            <p><strong>Total a Pagar:</strong> ${total_to_pay:.2f}</p>
                            <p><strong>Monto Pagado:</strong> ${payment_amount:.2f}</p>
                            <p><strong>Cambio a Devolver:</strong> ${change_amount:.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if invoice_button and selected_appointment:
                        if payment_amount < total_to_pay:
                            st.markdown("<div class='error-message'>El monto pagado debe ser mayor o igual al total a pagar.</div>", unsafe_allow_html=True)
                        else:
                            # Guardar la factura en la base de datos
                            invoice_id = save_invoice(selected_appointment_id, total_to_pay, payment_amount, change_amount, late_fee, discount)
                            
                            if invoice_id:
                                # Crear directorio para facturas si no existe
                                if not os.path.exists('facturas'):
                                    os.makedirs('facturas')
                                
                                # Generar archivo de factura
                                invoice_filename = f"facturas/factura_{invoice_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
                                
                                # Crear contenido de la factura (58mmx40mm)
                                invoice_content = f"""
===============================
      LUCERO GLAM STUDIO
===============================
Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
No. Factura: {invoice_id}

Cliente: {selected_appointment[2]} {selected_appointment[3]}
Servicio: {selected_appointment[5]}
Fecha Cita: {datetime.datetime.strptime(selected_appointment[7], '%Y-%m-%d %H:%M').strftime('%d/%m/%Y %H:%M')}

-------------------------------
Precio Servicio:    ${service_price:.2f}
Apartado Pagado:    ${deposit_amount:.2f}
Monto Restante:     ${remaining_amount:.2f}
Mora:               ${late_fee:.2f}
Descuento:          ${discount:.2f}
-------------------------------
TOTAL A PAGAR:      ${total_to_pay:.2f}
PAGADO CON:         ${payment_amount:.2f}
CAMBIO:             ${change_amount:.2f}
-------------------------------

      ¡GRACIAS POR SU VISITA!
      Tel: +1 849-532-0716
===============================
"""
                                
                                # Guardar la factura en un archivo
                                with open(invoice_filename, 'w') as f:
                                    f.write(invoice_content)
                                
                                # Marcar la cita como completada
                                mark_appointment_as_completed(selected_appointment_id)
                                
                                # Guardar en variables de sesión
                                st.session_state.invoice_generated = True
                                st.session_state.invoice_filename = invoice_filename
                                st.session_state.invoice_content = invoice_content
                                st.session_state.invoice_id = invoice_id
                                
                                # Recargar la página para mostrar la factura
                                st.rerun()
                            else:
                                st.markdown("<div class='error-message'>Error al generar la factura. Intente nuevamente.</div>", unsafe_allow_html=True)
            
            # Si ya se generó una factura, mostrar los resultados y el botón de descarga
            if st.session_state.invoice_generated:
                st.markdown(f"<div class='success-message'>¡Factura generada exitosamente!</div>", unsafe_allow_html=True)
                
                # Mostrar la factura en la interfaz
                st.text_area("Vista previa de la factura", st.session_state.invoice_content, height=400)
                
                # Botón de descarga para la factura (fuera del formulario)
                with open(st.session_state.invoice_filename, "r") as file:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Descargar Factura",
                            data=file,
                            file_name=f"Factura_LuceroGlamStudio_{st.session_state.invoice_id}.txt",
                            mime="text/plain"
                        )
                
                # Botón para imprimir directamente
                with col2:
                    # Formatear el contenido para impresión
                    formatted_content = st.session_state.invoice_content.replace("\n", "<br>")
                    # Crear el componente HTML con JavaScript para imprimir
                    print_button_html = f"""
                    <button 
                        onclick="printInvoice()" 
                        style="
                            background-color: #4CAF50; 
                            color: white; 
                            padding: 0.5rem 1rem; 
                            border: none; 
                            border-radius: 4px; 
                            cursor: pointer; 
                            font-size: 1rem;
                            width: 100%;
                        "
                    >Imprimir Factura</button>
                    
                    <div id="printContent" style="display:none;">
                        <div style="font-family: monospace; font-size: 9pt; line-height: 1.1;">{formatted_content}</div>
                    </div>
                    
                    <script>
                    function printInvoice() {{
                        const printWindow = window.open('', '_blank');
                        printWindow.document.write('<html><head><title>Factura Lucero Glam Studio</title>');
                        printWindow.document.write(`
                            <style>
                                @page {{ size: 80mm auto; margin: 0mm; }}
                                body {{ 
                                    width: 80mm; 
                                    margin: 0; 
                                    padding: 0; 
                                    font-family: monospace; 
                                    font-size: 9pt; 
                                    line-height: 1.1;
                                }}
                                div {{ 
                                    width: 100%; 
                                    white-space: pre-wrap; 
                                    page-break-inside: avoid; 
                                }}
                            </style>
                        `);
                        printWindow.document.write('</head><body>');
                        printWindow.document.write(document.getElementById('printContent').innerHTML);
                        printWindow.document.write('</body></html>');
                        printWindow.document.close();
                        printWindow.focus();
                        setTimeout(function() {{
                            printWindow.print();
                            printWindow.close();
                        }}, 250);
                    }}
                    </script>
                    """
                    components.html(print_button_html, height=50)
                
                # Mensaje de servicio completado
                st.markdown("<div class='success-message'>¡Servicio completado exitosamente!</div>", unsafe_allow_html=True)
                st.markdown("<div class='info-message'>Puede imprimir la factura descargándola y enviándola a su impresora.</div>", unsafe_allow_html=True)
                
                # Botón para crear una nueva factura
                if st.button("Crear Nueva Factura"):
                    st.session_state.invoice_generated = False
                    st.rerun()

# Main content area
st.markdown("<h2 class='subheader'>Bienvenido a Lucero Glam Studio App</h2>", unsafe_allow_html=True)
st.write("""
Esta aplicación le permite administrar su negocio de maquillaje de manera eficiente.
Utilice el panel lateral para registrar nuevos clientes y servicios, así como gestionar los existentes.
""")

# Create tabs for different statistics
tab1, tab2, tab3 = st.tabs(["Clientes Recientes", "Servicios Disponibles", "Citas Próximas"])

# Tab for recent clients
with tab1:
    st.markdown("<h3>Clientes Recientes</h3>", unsafe_allow_html=True)
    recent_clients = get_all_clients()

    if recent_clients:
        # Convert to DataFrame for better display
        df = pd.DataFrame(recent_clients, columns=["ID", "Nombre", "Apellido", "Teléfono", "Descripción", "Fecha de Registro"])
        
        # Display only the most recent clients (limited to 10)
        st.dataframe(df[["Nombre", "Apellido", "Teléfono"]].head(10), use_container_width=True)
    else:
        st.info("No hay clientes registrados aún. Utilice el panel lateral para registrar nuevos clientes.")

# Tab for available services
with tab2:
    st.markdown("<h3>Servicios Disponibles</h3>", unsafe_allow_html=True)
    services = get_all_services()

    if services:
        # Convert to DataFrame for better display
        services_df = pd.DataFrame(services, columns=["ID", "Nombre", "Descripción", "Precio", "Duración (min)"])
        
        # Format price with currency symbol
        services_df["Precio"] = services_df["Precio"].apply(lambda x: f"${x:.2f}")
        
        # Display services in a table
        st.dataframe(services_df[["Nombre", "Precio", "Duración (min)", "Descripción"]], use_container_width=True)
        
        # Show a summary of services
        st.markdown("<h4>Resumen de Servicios</h4>", unsafe_allow_html=True)
        total_services = len(services)
        avg_price = sum([service[3] for service in services]) / total_services if total_services > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Servicios", total_services)
        with col2:
            st.metric("Precio Promedio", f"${avg_price:.2f}")
        with col3:
            min_price = min([service[3] for service in services]) if services else 0
            max_price = max([service[3] for service in services]) if services else 0
            st.metric("Rango de Precios", f"${min_price:.2f} - ${max_price:.2f}")
    else:
        st.info("No hay servicios registrados aún. Utilice el panel lateral para registrar nuevos servicios.")

# Tab for upcoming appointments
with tab3:
    st.markdown("<h3>Citas Próximas</h3>", unsafe_allow_html=True)
    
    # Get today's date
    today = datetime.datetime.now().date()
    
    # Get appointments for today and future dates
    upcoming_appointments = []
    all_appointments = get_all_appointments()
    
    for appointment in all_appointments:
        appointment_date = datetime.datetime.strptime(appointment[4], "%Y-%m-%d %H:%M").date()
        if appointment_date >= today and appointment[7] == "scheduled":  # Only show scheduled appointments
            upcoming_appointments.append(appointment)
    
    if upcoming_appointments:
        # Convert to DataFrame for better display
        df = pd.DataFrame(upcoming_appointments, 
                         columns=["ID", "Nombre", "Apellido", "Servicio", "Fecha y Hora", "Apartado ($)", "Notas", "Estado"])
        
        # Format date and deposit amount
        df["Fecha y Hora"] = pd.to_datetime(df["Fecha y Hora"])
        df = df.sort_values(by="Fecha y Hora")
        df["Fecha"] = df["Fecha y Hora"].dt.strftime("%d/%m/%Y")
        df["Hora"] = df["Fecha y Hora"].dt.strftime("%H:%M")
        df["Apartado ($)"] = df["Apartado ($)"].apply(lambda x: f"${x:.2f}")
        
        # Display upcoming appointments in a table
        st.dataframe(df[["Nombre", "Apellido", "Servicio", "Fecha", "Hora", "Apartado ($)"]], use_container_width=True)
        
        # Show a summary of appointments
        st.markdown("<h4>Resumen de Citas</h4>", unsafe_allow_html=True)
        
        # Group by date to show appointments per day
        appointments_by_date = df.groupby("Fecha").size().reset_index(name="Cantidad")
        appointments_by_date = appointments_by_date.sort_values(by="Fecha")
        
        # Calculate total income from upcoming appointments
        total_deposits = sum([float(appointment[5]) for appointment in upcoming_appointments])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Citas Próximas", len(upcoming_appointments))
        with col2:
            st.metric("Total Apartado", f"${total_deposits:.2f}")
        
        # Show appointments by date
        st.markdown("<h4>Citas por Día</h4>", unsafe_allow_html=True)
        st.bar_chart(appointments_by_date.set_index("Fecha"))
    else:
        st.info("No hay citas próximas programadas. Utilice la sección de Citas en el panel lateral para agendar nuevas citas.")
