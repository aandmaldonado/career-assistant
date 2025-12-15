import streamlit as st
from dotenv import load_dotenv
from app.core.profile import load_portfolio

# Load env vars
load_dotenv()


st.set_page_config(
    page_title="Career Assistant AI",
    page_icon="🚀",
    layout="wide"
)

def main():
    st.title("🚀 Career Assistant AI")
    st.markdown("""
    *Tu estratega de carrera personal. Analiza ofertas, investiga empresas y decide inteligentemente.*
    """)
    
    # 1. Load Portfolio
    try:
        portfolio = load_portfolio()
        with st.sidebar:
            st.success(f"✅ Perfil Cargado: **{portfolio.personal_info.name}**")
            st.info(f"📍 {portfolio.personal_info.title}")
            
            with st.expander("Ver Deal Breakers"):
                cond = portfolio.professional_conditions
                st.write(f"**Remoto:** {cond.availability.get('remote_work', 'N/A')}")
                st.write(f"**Visa:** {cond.work_permit.get('status', 'N/A')}")
    except Exception as e:
        st.error(f"Error cargando portfolio.yaml: {e}")
        return

    # 2. Input Section
    st.header("1. Ingresa la Oferta")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        job_url = st.text_input("URL de la oferta (LinkedIn, Glassdoor...)", placeholder="https://...")
    
    with col2:
        job_text = st.text_area("O pega la descripción completa aquí", height=150, placeholder="Senior Software Engineer needed...")

    analyze_btn = st.button("🕵️‍♂️ Analizar Oferta", type="primary", use_container_width=True)

    if analyze_btn:
        if not job_text and not job_url:
            st.warning("Por favor ingresa una URL o el texto de la oferta.")
            return

        with st.status("🔍 Procesando oferta...") as status:
            final_text = job_text
            
            if job_url:
                try:
                    status.update(label="🌍 Extrayendo contenido de la URL...", state="running")
                    from app.tools.scraper import scrape_job_url
                    scraped_text = scrape_job_url(job_url)
                    final_text = scraped_text + "\n\n" + job_text # Append manual text if any
                    status.write("✅ Contenido extraído exitosamente.")
                except Exception as e:
                    st.error(f"Error extrayendo URL: {e}")
                    status.update(label="❌ Falló la extracción", state="error")
                    return

            st.write("📄 Texto recuperado (Preview primeros 500 chars):")
            st.code(final_text[:500] + "...")
            
            # 3. Agent Analysis
            status.update(label="🧠 Analizando compatibilidad (Agent)...", state="running")
            from app.core.agent import CareerAgent
            
            try:
                agent = CareerAgent(portfolio)
                
                # Step 3.1: Extract Company & Deep Research
                status.update(label="🕵️‍♂️ Investigando empresa (Búsqueda Profunda)...", state="running")
                company_name = agent.extract_company_name(final_text)
                research_context = ""
                
                # Filter generic names
                if company_name and company_name.lower() not in ["unknown", "confidential", "cliente final"]:
                    st.write(f"🏢 Empresa detectada: **{company_name}**. Buscando referencias...")
                    research_context = agent.perform_research(company_name)
                    with st.expander("🌐 Resultados de Investigación Web", expanded=False):
                        st.markdown(research_context)
                else:
                    st.warning(f"⚠️ No se pudo detectar un nombre de empresa específico (Detectado: '{company_name}'). Se omitirá la investigación web.")

                # Step 3.2: Final Analysis
                status.update(label="🧠 Analizando compatibilidad final...", state="running")
                result = agent.analyze(final_text, research_context=research_context)
                
                status.write("✅ Análisis completado.")
                
                # --- Result Display ---
                st.divider()
                st.subheader(f"Veredicto: {result.verdict}")
                
                # Score Metric
                col_score, col_summary = st.columns([1, 3])
                with col_score:
                    st.metric("Puntuación de Match", f"{result.match_score}%")
                with col_summary:
                    st.write(f"**Resumen:** {result.reasoning_summary}")

                # Hard Filters
                if result.hard_filter_check:
                    hf = result.hard_filter_check
                    with st.expander("🔍 Detalles Filtros Duros (Hard Filters)", expanded=True):
                         c1, c2, c3 = st.columns(3)
                         c1.checkbox("Remoto", value=hf.remote_pass, disabled=True)
                         c2.checkbox("Visa Sponsorship", value=hf.visa_pass, disabled=True)
                         c3.checkbox("Salario (>52k)", value=hf.salary_pass, disabled=True)
                
                # Pros & Cons
                col_pros, col_cons = st.columns(2)
                with col_pros:
                    st.success("✅ Fortalezas / Pros")
                    for item in result.pros:
                        st.write(f"- {item}")
                        
                with col_cons:
                    st.warning("⚠️ Riesgos / Contras")
                    for item in result.cons:
                        st.write(f"- {item}")
                        
                # Raw JSON for debug
                with st.expander("Ver JSON Completo (Debug)"):
                     st.json(result.model_dump())

            except Exception as e:
                st.error(f"Error en Agente: {e}")
                status.update(label="❌ Error Fatal", state="error")
            
            status.update(label="✅ Proceso Finalizado", state="complete", expanded=False)

if __name__ == "__main__":
    main()
