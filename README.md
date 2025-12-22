# EventScale API 🚀

> **Backend para Sistema de Gestión de Eventos y Portafolio Profesional**

![EventScale Status](https://img.shields.io/badge/Status-In%20Progress-orange?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791?style=flat-square&logo=postgresql)

**EventScale** es una API backend de alto rendimiento diseñada para gestionar la venta masiva de entradas, la administración de usuarios y la seguridad, sirviendo como núcleo lógico para el cliente frontend.

## 🔌 Integración con el Cliente (Frontend)

Este backend actúa como la API RESTful que alimenta al proyecto **Portafolio Profesional & Sistema de Gestión (React + Vite)**.

* **Repositorio Frontend:** [Portafolio & Dashboard](https://github.com/DavidAlarcon1803/portafolio.git)
* **🚀 Demo del Cliente:** [https://portafolio-blond-five-68.vercel.app/](https://portafolio-blond-five-68.vercel.app/)

La API proporciona los endpoints necesarios para:
1.  **Autenticación:** Login para el Dashboard administrativo.
2.  **Gestión de Usuarios:** Datos para la tabla `UsersManager` del dashboard.
3.  **Lógica de Negocio:** Compra de tickets y gestión de eventos.

---

## 🎯 Objetivo del Proyecto

Crear una arquitectura robusta y escalable capaz de manejar problemas complejos de concurrencia (como "race conditions" en la venta de tickets) y procesar tareas pesadas en segundo plano, demostrando un perfil **Full Stack** avanzado.

## 🏗️ Arquitectura y Despliegue

El sistema está desplegado utilizando una infraestructura moderna y distribuida:

* **API Host:** [Railway](https://railway.app/)
* **Base de Datos:** [Neon Tech](https://console.neon.tech/) (PostgreSQL Serverless con optimización SSL).
* **Cola de Mensajes:** [CloudAMQP](https://www.cloudamqp.com/) (RabbitMQ).
* **Frontend:** Vercel (Consumo vía Fetch API).

