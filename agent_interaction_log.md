# Historial de Ingeniería Agéntica (Interaction Log)
**Proyecto**: Sistema de Análisis de Compatibilidad Laboral (D&D Ind. / TechCorp)
**Fecha de Release**: 19 de Marzo, 2026
**Fase Actual**: Code Freeze (RC V1.0)

Este documento detalla cronológicamente la evolución del desarrollo asistido por IAG (Inteligencia Artificial Generativa) a través de "Agentes Especializados", detallando el traspaso de información y las resoluciones técnicas que llevaron al producto actual.

---

## 1. Requerimientos Iniciales y Visión (Día 1)
El requerimiento base fue construir un sistema de validación de perfiles técnicos de candidatos (Ingenieros) contra Ofertas Laborales específicas, utilizando la API de Google Gemini como motor de "MatchMaker".

**Desafíos Iniciales:**
- Definición de Entidades Claras (Candidate, JobOffer).
- Modularidad: Se propuso y aceptó usar **Clean Architecture** para que la API, los casos de uso (LLM) y la persistencia estuvieran desacoplados.

## 2. Decisiones de Arquitectura Tomadas en Conjunto
A través del **Arquitecto (Agente Principal)**, se estructuró la aplicación en Flask bajo el patrón `/app`:
- `infrastructure/api/routes.py`: Capa de red (Flask Blueprints).
- `use_cases/matchmaker.py`: Lógica de inyección de LLM.
- `infrastructure/services/gemini_service.py`: Wrapper de la API de Google, incluyendo un sistema de **Fallback Reversivo** (intentando primero `gemini-1.5-pro`, cayendo a `gemini-1.5-flash` en caso de error de disponibilidad o Rate Limits).

## 3. Handoffs (Delegaciones entre Agentes)

### A. Del Arquitecto al Portero (Backend Endpoint)
El **Portero** recibió la misión de crear el endpoint `/api/v1/match`. 
- Se implementó un "Smart Parser" para tolerar diferentes formatos de JSON entrantes (objetos planos, anidados bajo la llave `{"json":...}`, o listas de n8n). Esto permitió flexibilidad en la ingesta de datos.

### B. Del Traductor (Prompt Engineer) al Frontend
El **Traductor** diseño un Prompt para que Gemini actuara como Reclutador Técnico, devolviendo un JSON estricto: `match_percentage`, `technical_pros`, `improvement_areas` y `market_relevance`.
- El **Frontend** tomó este esquema y diseñó un Dashboard en HTML/Vanilla JS y Bootstrap 5 para consumir dicho JSON renderizando colores semánticos y barras de progreso fluidas.

### C. La Misión "Prospección Autónoma" (n8n)
Pivotamos de un modelo manual a uno automatizado (Outbound):
1. **Frontend**: Removió el formulario de oferta y habilitó la carga de CV PDF y preferencias en un solo clic.
2. **Portero**: Creó `/api/v1/sync-search` para tomar esos datos y enviarlos a un **Webhook de n8n**.
3. **Database**: Se construyó un poll asíncrono que consulta en ciclo la base local SQLite `discoveries.db` para pintar oportunidades a medida que n8n las va encontrando y enviando de regreso mediante el endpoint `/discovery`.

## 4. Resolución de Bugs Clave

### A. El Bloqueo del Portero (400 Bad Request)
- **Problema**: n8n y Powershell enviaban estructuras JSON dispares, causando fallos de esquema en el servidor Flask.
- **Resolución**: El Portero implementó recursividad en la lectura de la request (`data.get("json", data)`), aplanando el payload antes de inyectarlo en la capa de Casos de Uso.

### B. Hot-Reloading y Pérdida de Datos SQLite (El Bug "DROP TABLE")
- **Problema**: Durante la auditoría visual con 20 ofertas, el Dashboard se renderizaba vacío a pesar de que la base de datos se reportaba poblada.
- **Root Cause**: Flask, al recargar módulos en modo *debug*, invocaba globalmente la inicialización de `DiscoveryRepository`, la cual poseía el comando `DROP TABLE IF EXISTS`.
- **Resolución**: Se removió el statement de "Drop", reemplazándolo por `CREATE TABLE IF NOT EXISTS`, logrando persistencia total de los resultados asíncronos sin importar reinicios del server.

### C. Ajuste de Neutralidad Absoluta
- **Problema**: El sub-agente navegador (Browser Agent) reportó que la IA de Gemini seguía generando textos con preferencias geográficas personales ("Europa/Irlanda").
- **Resolución**: Modificación estricta en `gemini_service.py` limitando el análisis puramente a las **Competencias Core de la Ingeniería**, y purga de la base de datos borrando referencias previas en los mockups.

---
**Firma**: Equipo de Ingeniería Agéntica (Arquitecto, Backend, Frontend, Traductor, Testing Sub-Agent).
**Estado Fina**: Lógica envuelta en UI Premium. Repositorio preparado para publicación GitHub (`.gitignore`, `requirements.txt`). Listo para demostración a Comisión de Proyecto de Título.
