
import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# -----------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------------

st.set_page_config(
    page_title="AGROSMART | Monitor Agrícola",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------
# VARIABLES DE ESTADO
# -----------------------------------------

if 'sensor_data' not in st.session_state:
    st.session_state.sensor_data = None

# -----------------------------------------
# FUNCIÓN MQTT ORIGINAL
# -----------------------------------------

def get_mqtt_message(broker, port, topic, client_id):

    message_received = {
        "received": False,
        "payload": None
    }

    def on_message(client, userdata, message):
        try:
            payload = json.loads(
                message.payload.decode("utf-8")
            )

            message_received["payload"] = payload
            message_received["received"] = True

        except:
            message_received["payload"] = (
                message.payload.decode("utf-8")
            )
            message_received["received"] = True

    try:
        client = mqtt.Client(client_id=client_id)

        client.on_message = on_message

        client.connect(broker, port, 60)
        client.subscribe(topic)
        client.loop_start()

        timeout = time.time() + 5

        while (
            not message_received["received"]
            and time.time() < timeout
        ):
            time.sleep(0.1)

        client.loop_stop()
        client.disconnect()

        return message_received["payload"]

    except Exception as e:
        return {"error": str(e)}


# -----------------------------------------
# ESTILOS CSS - AGROSMART
# -----------------------------------------

st.markdown("""
<style>

/* FONDO */

.stApp {
    background:
        radial-gradient(circle at 10% 5%,
        rgba(71, 130, 73, 0.18), transparent 35%),
        linear-gradient(135deg,
        #10251b 0%, #142e20 55%, #0d2017 100%);
    color: white;
}

/* OCULTAR ELEMENTOS */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* CONTENEDOR */

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* TEXTOS */

h1, h2, h3 {
    color: #ffffff !important;
}

p {
    color: #c5d9c8;
}

/* ENCABEZADO */

.hero {
    background: linear-gradient(120deg,
        #285c38, #387b49);
    padding: 32px;
    border-radius: 22px;
    border: 1px solid #548b60;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
}

.hero-title {
    color: white;
    font-size: 43px;
    font-weight: 900;
    letter-spacing: 2px;
    margin: 0;
}

.hero-title span {
    color: #b9ee8e;
}

.hero-subtitle {
    color: #e0f1df;
    font-size: 15px;
    letter-spacing: 2px;
    margin-top: 8px;
}

.hero-description {
    color: #e0f1df;
    font-size: 15px;
    margin-top: 18px;
}

/* SECCIONES */

.section-title {
    font-size: 23px;
    color: #ffffff;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* TARJETAS DE INFORMACIÓN */

.info-card {
    background: #1b3828;
    border: 1px solid #365d40;
    border-radius: 17px;
    padding: 22px;
    margin-bottom: 15px;
}

/* MÉTRICAS */

.metric-card {
    background: linear-gradient(145deg,
        #20442d, #193525);
    border: 1px solid #426d4b;
    border-radius: 18px;
    padding: 22px;
    min-height: 145px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

.metric-icon {
    font-size: 27px;
}

.metric-label {
    color: #b6d4bb;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 12px;
}

.metric-value {
    color: #ffffff;
    font-size: 29px;
    font-weight: 800;
    margin-top: 8px;
    overflow-wrap: anywhere;
}

/* BOTONES */

.stButton button {
    background: linear-gradient(120deg,
        #65a84c, #83c65b);
    color: #10251b;
    font-weight: 800;
    border: none;
    border-radius: 12px;
    min-height: 48px;
    transition: 0.3s;
}

.stButton button:hover {
    background: #a1db78;
    color: #10251b;
    border: none;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #10251b;
    border-right: 1px solid #31543a;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #a8db8a !important;
}

/* CAMPOS */

.stTextInput input,
.stNumberInput input {
    background: #1b3828;
    color: white;
    border: 1px solid #426d4b;
    border-radius: 9px;
}

div[data-baseweb="select"] > div {
    background: #1b3828;
    border-color: #426d4b;
}

/* ALERTAS */

.alert-good {
    background: #1e5030;
    border-left: 5px solid #83d66b;
    color: #d7f5d2;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.alert-warning {
    background: #5a481f;
    border-left: 5px solid #e9c45e;
    color: #ffedb6;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}

/* PIE */

.footer {
    text-align: center;
    color: #91ad96;
    font-size: 12px;
    letter-spacing: 1px;
    padding: 25px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------------
# SIDEBAR - CONFIGURACIÓN
# -----------------------------------------

with st.sidebar:

    st.markdown("## 🌱 AGROSMART")

    st.caption("SISTEMA DE MONITOREO AGRÍCOLA")

    st.divider()

    st.subheader("⚙️ Conexión MQTT")

    broker = st.text_input(
        "Broker MQTT",
        value="broker.mqttdashboard.com",
        help="Dirección del servidor MQTT"
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
        "ID del Cliente",
        value="streamlit_client"
    )

    st.divider()

    st.subheader("🌾 Información agrícola")

    finca = st.text_input(
        "Nombre de la finca",
        value="Mi finca"
    )

    cultivo = st.selectbox(
        "Tipo de cultivo",
        [
            "Café",
            "Maíz",
            "Arroz",
            "Tomate",
            "Papa",
            "Frijol",
            "Otro"
        ]
    )

    st.divider()

    st.caption("AGROSMART | Tecnología para el campo")


# -----------------------------------------
# ENCABEZADO PRINCIPAL
# -----------------------------------------

st.markdown("""
<div class="hero">

    <div class="hero-title">
        AGRO<span>SMART</span> 🌱
    </div>

    <div class="hero-subtitle">
        AGRICULTURA INTELIGENTE
    </div>

    <div class="hero-description">
        Monitorea las condiciones de tus cultivos
        y consulta los datos de tus sensores
        desde un solo lugar.
    </div>

</div>
""", unsafe_allow_html=True)


# -----------------------------------------
# INFORMACIÓN DE LA FINCA
# -----------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="info-card">
        <div style="color:#a8db8a;font-size:13px;font-weight:bold;">
            🌾 FINCA
        </div>
        <div style="font-size:23px;font-weight:800;color:white;">
            {finca}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="info-card">
        <div style="color:#a8db8a;font-size:13px;font-weight:bold;">
            🌱 CULTIVO
        </div>
        <div style="font-size:23px;font-weight:800;color:white;">
            {cultivo}
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------
# PANEL DE MONITOREO
# -----------------------------------------

st.markdown("""
<div class="section-title">
    📡 Panel de monitoreo
</div>
""", unsafe_allow_html=True)

st.write(
    "Consulta las mediciones enviadas por tus sensores agrícolas."
)

if st.button(
    "🔄  OBTENER DATOS DEL SENSOR",
    use_container_width=True
):

    with st.spinner("Conectando con los sensores..."):

        sensor_data = get_mqtt_message(
            broker,
            int(port),
            topic,
            client_id
        )

        st.session_state.sensor_data = sensor_data


# -----------------------------------------
# MOSTRAR RESULTADOS
# -----------------------------------------

if st.session_state.sensor_data is not None:

    st.markdown("""
    <div class="section-title">
        📊 Datos del cultivo
    </div>
    """, unsafe_allow_html=True)

    data = st.session_state.sensor_data

    # Verificar errores

    if isinstance(data, dict) and "error" in data:

        st.error(
            f"❌ Error de conexión: {data['error']}"
        )

    elif data is None:

        st.warning(
            "⚠️ No se recibieron datos. "
            "Verifica que el sensor esté publicando mensajes."
        )

    else:

        st.success("✅ Datos recibidos correctamente")

        # Mostrar métricas dinámicas

        if isinstance(data, dict):

            cols = st.columns(
                min(len(data), 4)
            )

            for i, (key, value) in enumerate(data.items()):

                with cols[i % len(cols)]:

                    # Iconos según nombre de variable

                    key_lower = key.lower()

                    if "temp" in key_lower:
                        icon = "🌡️"

                    elif "hum" in key_lower:
                        icon = "💧"

                    elif "soil" in key_lower or "suelo" in key_lower:
                        icon = "🌱"

                    elif "pres" in key_lower:
                        icon = "🌤️"

                    else:
                        icon = "📊"

                    st.markdown(f"""
                    <div class="metric-card">

                        <div class="metric-icon">
                            {icon}
                        </div>

                        <div class="metric-label">
                            {key.upper()}
                        </div>

                        <div class="metric-value">
                            {value}
                        </div>

                    </div>
                    """, unsafe_allow_html=True)

            # -----------------------------------------
            # RECOMENDACIONES INFORMATIVAS
            # -----------------------------------------

            st.markdown("""
            <div class="section-title">
                🌿 Información del cultivo
            </div>
            """, unsafe_allow_html=True)

            recommendations = []

            for key, value in data.items():

                key_lower = key.lower()

                try:
                    numeric_value = float(value)
                except (ValueError, TypeError):
                    continue

                if "temp" in key_lower:

                    if numeric_value >= 35:
                        recommendations.append(
                            ("warning",
                             "🌡️ Temperatura elevada. "
                             "Vigila las condiciones del cultivo.")
                        )

                    elif numeric_value <= 10:
                        recommendations.append(
                            ("warning",
                             "❄️ Temperatura baja. "
                             "Revisa las condiciones ambientales.")
                        )

                    else:
                        recommendations.append(
                            ("good",
                             "✅ Temperatura registrada sin alerta.")
                        )

                elif "hum" in key_lower and "suelo" not in key_lower:

                    if numeric_value < 35:
                        recommendations.append(
                            ("warning",
                             "💧 Humedad ambiental baja. "
                             "Vigila el ambiente del cultivo.")
                        )

                    elif numeric_value > 85:
                        recommendations.append(
                            ("warning",
                             "💧 Humedad ambiental elevada. "
                             "Vigila la ventilación del cultivo.")
                        )

                    else:
                        recommendations.append(
                            ("good",
                             "✅ Humedad ambiental registrada sin alerta.")
                        )

            if recommendations:

                for level, message in recommendations:

                    css_class = (
                        "alert-warning"
                        if level == "warning"
                        else "alert-good"
                    )

                    st.markdown(
                        f'<div class="{css_class}">{message}</div>',
                        unsafe_allow_html=True
                    )

            # -----------------------------------------
            # JSON COMPLETO
            # -----------------------------------------

            with st.expander("🔍 Ver información completa del sensor"):

                st.json(data)

        else:

            st.markdown("""
            <div class="info-card">
                <div class="metric-label">
                    MENSAJE RECIBIDO
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.code(data)


# -----------------------------------------
# ESTADO INICIAL
# -----------------------------------------

else:

    st.markdown("""
    <div class="info-card">

        <div style="font-size:40px;text-align:center;">
            🌱
        </div>

        <div style="font-size:21px;font-weight:800;
                    text-align:center;color:white;">
            Tu cultivo bajo control
        </div>

        <p style="text-align:center;color:#b8d4bd;">
            Presiona el botón de actualización para recibir
            información de tus sensores mediante MQTT.
        </p>

    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------
# PIE DE PÁGINA
# -----------------------------------------

st.markdown("""
<div class="footer">
    🌱 AGROSMART · AGRICULTURA INTELIGENTE
    <br><br>
    MONITOREO DE CULTIVOS MEDIANTE TECNOLOGÍA MQTT
</div>
""", unsafe_allow_html=True)
