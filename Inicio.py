
import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="AGROSMART",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ESTILOS CSS
# ==========================================

st.markdown("""
<style>

/* Fondo completo */
.stApp {
    background: linear-gradient(
        135deg,
        #e8f1e4 0%,
        #dcebd8 50%,
        #cfe3ca 100%
    );
}

[data-testid="stAppViewContainer"] {
    background: transparent;
}

[data-testid="stMain"] {
    background: transparent;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* Barra lateral */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #153d29 0%,
        #205638 55%,
        #2d6843 100%
    );
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Campos de la barra lateral */
[data-testid="stSidebar"] input {
    background-color: #ffffff !important;
    color: #173e2b !important;
    -webkit-text-fill-color: #173e2b !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] {
    color: #173e2b !important;
}

/* Título Configuración MQTT */
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

/* Tipografía */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* Títulos principales */
h1 {
    color: #19452d !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #285b39 !important;
    font-weight: 700 !important;
}

/* Texto general */
p, label {
    color: #385a43;
}

/* Botón principal */
.stButton > button {
    background: linear-gradient(90deg, #28633e, #3b8050) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: none !important;
    border-radius: 12px;
    height: 48px;
    font-weight: 700;
    transition: 0.2s;
}

/* Texto interno del botón */
.stButton > button p,
.stButton > button span,
.stButton > button div {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Hover del botón */
.stButton > button:hover {
    background: #19452d !important;
    color: #ffffff !important;
    border: none !important;
}

/* Métricas */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #d4e5d0;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 5px 15px rgba(30, 70, 40, 0.08);
}

[data-testid="stMetricLabel"] {
    color: #63816a !important;
}

[data-testid="stMetricValue"] {
    color: #245b38 !important;
}

/* Expansores */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.75);
    border: 1px solid #d3e3ce;
    border-radius: 13px;
}

/* Campos de texto */
.stTextInput input,
.stNumberInput input {
    border-radius: 9px;
}

/* Alertas */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Separadores */
hr {
    border-color: #c6dbc0;
}

/* Pie de página */
.footer {
    text-align: center;
    color: #65816a;
    font-size: 13px;
    padding: 25px 0 10px 0;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# VARIABLES DE SESIÓN
# ==========================================

if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = None

if "last_update" not in st.session_state:
    st.session_state.last_update = None


# ==========================================
# FUNCIÓN DE CONEXIÓN MQTT
# ==========================================

def get_mqtt_message(broker, port, topic, client_id):

    message_received = {
        "received": False,
        "payload": None
    }

    def on_message(client, userdata, message):
        try:
            payload = json.loads(message.payload.decode())
            message_received["payload"] = payload
            message_received["received"] = True

        except Exception:
            message_received["payload"] = message.payload.decode()
            message_received["received"] = True

    client = None

    try:
        client = mqtt.Client(client_id=client_id)
        client.on_message = on_message

        client.connect(broker, int(port), 60)
        client.subscribe(topic)
        client.loop_start()

        timeout = time.time() + 5

        while not message_received["received"] and time.time() < timeout:
            time.sleep(0.1)

        client.loop_stop()
        client.disconnect()

        if message_received["received"]:
            return message_received["payload"]

        return {
            "error": "No se recibieron datos dentro del tiempo de espera."
        }

    except Exception as e:

        if client is not None:
            try:
                client.loop_stop()
                client.disconnect()
            except Exception:
                pass

        return {"error": str(e)}


# ==========================================
# BARRA LATERAL
# ==========================================

with st.sidebar:

    st.title("🌱 AGROSMART")

    st.markdown(
        "<h3 style='color: white !important;'>Configuración MQTT</h3>",
        unsafe_allow_html=True
    )

    st.write("Conecta tu sistema de sensores agrícolas.")

    st.divider()

    broker = st.text_input(
        "Broker MQTT",
        value="broker.mqttdashboard.com"
    )

    port = st.number_input(
        "Puerto",
        value=1883,
        min_value=1,
        max_value=65535
    )

    topic = st.text_input(
        "Tópico",
        value="Sensor/THP2"
    )

    client_id = st.text_input(
        "ID del cliente",
        value="agrosmart_client"
    )

    st.divider()

    st.markdown("### 🌾 Información de la finca")

    finca = st.text_input(
        "Nombre de la finca",
        value="Mi finca"
    )

    cultivo = st.selectbox(
        "Tipo de cultivo",
        [
            "Tomate",
            "Maíz",
            "Café",
            "Lechuga",
            "Aguacate",
            "Flores",
            "Otro"
        ]
    )

    st.divider()

    st.caption("AGROSMART | Agricultura inteligente")


# ==========================================
# ENCABEZADO
# ==========================================

st.title("🌱 AGROSMART")

st.subheader("AGRICULTURA INTELIGENTE")

st.write(
    "Monitorea las condiciones de tus cultivos y consulta "
    "los datos de tus sensores desde un solo lugar."
)

st.divider()


# ==========================================
# INFORMACIÓN DE LA FINCA
# ==========================================

st.subheader("🌾 Información de tu finca")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Finca registrada",
        value=finca
    )

with col2:
    st.metric(
        label="Cultivo seleccionado",
        value=cultivo
    )


# ==========================================
# INFORMACIÓN DE USO
# ==========================================

with st.expander("ℹ️ ¿Cómo utilizar AGROSMART?"):

    st.markdown("""
    1. Configura el broker MQTT en el menú lateral.
    2. Ingresa el puerto y el tópico de tu sensor.
    3. Escribe un identificador para el cliente.
    4. Presiona el botón **Obtener datos del sensor**.
    5. Consulta las mediciones recibidas.

    **Brokers públicos para pruebas:**

    - broker.mqttdashboard.com
    - test.mosquitto.org
    - broker.hivemq.com
    """)


# ==========================================
# CONEXIÓN CON EL SENSOR
# ==========================================

st.divider()

st.subheader("📡 Conexión con los sensores")

if st.button(
    "🔄 Obtener datos del sensor",
    use_container_width=True
):

    with st.spinner("Conectando al broker y esperando datos..."):

        sensor_data = get_mqtt_message(
            broker,
            int(port),
            topic,
            client_id
        )

        st.session_state.sensor_data = sensor_data
        st.session_state.last_update = time.strftime("%H:%M:%S")

        st.rerun()


# ==========================================
# VISUALIZACIÓN DE DATOS
# ==========================================

if st.session_state.sensor_data is not None:

    st.divider()

    st.subheader("📊 Monitor de condiciones agrícolas")

    data = st.session_state.sensor_data

    if isinstance(data, dict) and "error" in data:

        st.error(f"❌ Error de conexión: {data['error']}")

    else:

        st.success("✅ Datos recibidos correctamente")

        if st.session_state.last_update:
            st.caption(
                f"Última actualización: {st.session_state.last_update}"
            )

        if isinstance(data, dict):

            temperatura = None
            humedad = None

            st.markdown("### 🌡️ Mediciones del sensor")

            if data:

                columnas = st.columns(min(len(data), 3))

                for i, (key, value) in enumerate(data.items()):

                    with columnas[i % len(columnas)]:

                        nombre = str(key).lower()
                        unidad = ""

                        try:
                            valor = float(value)

                            if "temp" in nombre:
                                unidad = " °C"
                                temperatura = valor

                            elif "hum" in nombre:
                                unidad = " %"
                                humedad = valor

                        except (ValueError, TypeError):
                            pass

                        st.metric(
                            label=str(key).replace("_", " ").title(),
                            value=f"{value}{unidad}"
                        )

            else:
                st.info("El mensaje recibido no contiene mediciones.")

            # Recomendaciones
            st.markdown("### 🌿 Recomendaciones para tu cultivo")

            if temperatura is not None:

                if temperatura < 15:
                    st.info(
                        "❄️ Temperatura baja: revisa si el cultivo "
                        "necesita protección frente al frío."
                    )

                elif temperatura <= 30:
                    st.success(
                        "🌱 Temperatura moderada: las condiciones "
                        "térmicas están dentro de un rango general moderado."
                    )

                else:
                    st.warning(
                        "☀️ Temperatura elevada: verifica la ventilación "
                        "y las necesidades de riego."
                    )

            if humedad is not None:

                if humedad < 40:
                    st.warning(
                        "💧 Humedad baja: comprueba las condiciones "
                        "de humedad y las necesidades de riego."
                    )

                elif humedad <= 70:
                    st.success(
                        "🌿 Humedad moderada: la medición está dentro "
                        "de un rango general moderado."
                    )

                else:
                    st.info(
                        "💦 Humedad elevada: revisa la ventilación "
                        "y la posible acumulación de humedad."
                    )

            with st.expander("📄 Ver información JSON completa"):
                st.json(data)

        else:

            st.markdown("### Mensaje recibido")
            st.code(data)


# ==========================================
# ESTADO INICIAL
# ==========================================

else:

    st.info(
        "🌱 Esperando datos del sensor. "
        "Configura tu conexión MQTT y presiona el botón "
        "para consultar las mediciones de tu cultivo."
    )


# ==========================================
# PIE DE PÁGINA
# ==========================================

st.divider()

st.markdown(
    """
    <div class="footer">
        🌱 AGROSMART | Sistema de monitoreo agrícola inteligente
    </div>
    """,
    unsafe_allow_html=True
)
