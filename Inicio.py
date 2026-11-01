
import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# ==========================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ==========================================

st.set_page_config(
    page_title="AGROSMART",
    page_icon="🌱",
    layout="wide"
)

# ==========================================
# ESTILOS CSS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f3f7ef 0%, #e7f0e2 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

[data-testid="stSidebar"] {
    background: #173e2b;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebar"] input {
    color: #173e2b !important;
    background: white !important;
}

[data-testid="stSidebar"] label {
    color: #e3f0e4 !important;
}

.hero {
    background: linear-gradient(120deg, #17452e, #34734a);
    padding: 42px 35px;
    border-radius: 24px;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(23, 62, 43, 0.15);
}

.hero-title {
    color: white;
    font-size: 46px;
    font-weight: 800;
    letter-spacing: 1px;
    margin: 0;
}

.hero-title span {
    color: #b9ed8d;
}

.hero-subtitle {
    color: #c9e7bd;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 4px;
    margin-top: 5px;
}

.hero-description {
    color: #edf6e9;
    font-size: 15px;
    margin-top: 20px;
    line-height: 1.7;
}

.section-title {
    color: #214c32;
    font-size: 23px;
    font-weight: 700;
    margin-top: 15px;
    margin-bottom: 15px;
}

.info-card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #dce9d9;
    box-shadow: 0 4px 15px rgba(25, 65, 40, 0.05);
    margin-bottom: 15px;
}

.info-label {
    color: #718477;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.info-value {
    color: #214c32;
    font-size: 25px;
    font-weight: 700;
    margin-top: 5px;
}

.info-icon {
    font-size: 27px;
}

.stButton > button {
    background: #34734a;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #245b38;
    color: white;
    border: none;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #dce9d9;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(25, 65, 40, 0.05);
}

div[data-testid="stMetricLabel"] {
    color: #718477;
}

div[data-testid="stMetricValue"] {
    color: #214c32;
}

.stAlert {
    border-radius: 12px;
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

        return {"error": "No se recibieron datos dentro del tiempo de espera."}

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

    st.markdown("## 🌱 AGROSMART")
    st.markdown("### Configuración MQTT")

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
# ENCABEZADO PRINCIPAL
# ==========================================

st.markdown("""
<div class="hero">
    <div class="hero-title">
        AGRO<span>SMART</span> 🌱
    </div>

    <div class="hero-subtitle">
        AGRICULTURA INTELIGENTE
    </div>

    <div class="hero-description">
        Monitorea las condiciones de tus cultivos y consulta
        los datos de tus sensores desde un solo lugar.
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# INFORMACIÓN GENERAL
# ==========================================

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="info-card">
        <div class="info-label">🌾 Finca registrada</div>
        <div class="info-value">{finca}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="info-card">
        <div class="info-label">🌱 Cultivo seleccionado</div>
        <div class="info-value">{cultivo}</div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# INFORMACIÓN DE USO
# ==========================================

with st.expander("ℹ️ ¿Cómo utilizar AGROSMART?"):

    st.markdown("""
    1. Configura el broker MQTT en el menú lateral.
    2. Ingresa el puerto y el tópico de tu sensor.
    3. Escribe un identificador para el cliente.
    4. Selecciona el botón **Obtener datos del sensor**.
    5. Consulta las mediciones recibidas en el panel.

    **Brokers públicos para realizar pruebas:**

    - broker.mqttdashboard.com
    - test.mosquitto.org
    - broker.hivemq.com
    """)


# ==========================================
# BOTÓN PARA OBTENER DATOS
# ==========================================

st.markdown(
    '<div class="section-title">📡 Conexión con los sensores</div>',
    unsafe_allow_html=True
)

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

    st.markdown(
        '<div class="section-title">📊 Monitor de condiciones agrícolas</div>',
        unsafe_allow_html=True
    )

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

            # Identificar temperatura y humedad para recomendaciones
            temperatura = None
            humedad = None

            for key, value in data.items():

                nombre = str(key).lower()

                try:
                    valor = float(value)

                    if "temp" in nombre:
                        temperatura = valor

                    elif "hum" in nombre:
                        humedad = valor

                except (ValueError, TypeError):
                    pass

            # Mostrar todas las mediciones recibidas
            st.markdown("### 🌡️ Mediciones del sensor")

            columnas = st.columns(min(len(data), 3))

            for i, (key, value) in enumerate(data.items()):

                with columnas[i % len(columnas)]:

                    unidad = ""

                    nombre = str(key).lower()

                    if "temp" in nombre:
                        unidad = " °C"

                    elif "hum" in nombre:
                        unidad = " %"

                    st.metric(
                        label=str(key).replace("_", " ").title(),
                        value=f"{value}{unidad}"
                    )

            # Recomendaciones básicas
            st.markdown("### 🌿 Recomendaciones para el cultivo")

            if temperatura is not None:

                if temperatura < 15:
                    st.info(
                        "❄️ **Temperatura baja:** "
                        "Revisa si el cultivo necesita protección frente al frío."
                    )

                elif temperatura <= 30:
                    st.success(
                        "🌱 **Temperatura moderada:** "
                        "Las condiciones térmicas están dentro de un rango general moderado."
                    )

                else:
                    st.warning(
                        "☀️ **Temperatura elevada:** "
                        "Verifica la ventilación y las necesidades de riego del cultivo."
                    )

            if humedad is not None:

                if humedad < 40:
                    st.warning(
                        "💧 **Humedad baja:** "
                        "Comprueba la humedad del suelo y las necesidades de riego."
                    )

                elif humedad <= 70:
                    st.success(
                        "🌿 **Humedad moderada:** "
                        "La humedad medida está dentro de un rango general moderado."
                    )

                else:
                    st.info(
                        "💦 **Humedad elevada:** "
                        "Revisa la ventilación y la posible acumulación de humedad."
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

    st.markdown("""
    <div class="info-card" style="text-align:center; padding:35px;">
        <div style="font-size:45px;">🌱</div>
        <h3 style="color:#214c32;">Esperando datos del sensor</h3>
        <p style="color:#718477;">
            Configura tu conexión MQTT y presiona el botón
            para consultar las mediciones de tu cultivo.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PIE DE PÁGINA
# ==========================================

st.markdown("""
<br>
<hr style="border:1px solid #dce9d9;">
<p style="
    text-align:center;
    color:#718477;
    font-size:12px;
">
    🌱 AGROSMART | Sistema de monitoreo agrícola inteligente
</p>
""", unsafe_allow_html=True)
