# Athena Glue S3 Data Processing Stack

## 📚 Descripción del Proyecto

Este proyecto implementa una arquitectura serverless para la exploración, catalogación y consulta de datos almacenados en Amazon S3, utilizando AWS Glue y AWS Athena. La infraestructura está definida como código (IaC) usando AWS CDK en Python.

El objetivo principal es facilitar el procesamiento y análisis de datos mediante:

- Creación automática de catálogos Glue sobre datos almacenados en S3.
- Consulta SQL mediante Athena.
- Orquestación de procesos mediante Step Functions.

---

## 🛠️ Arquitectura

```plaintext
[S3 Buckets]
   |
   | (Glue Crawler)
   v
[AWS Glue Data Catalog] <---> [AWS Athena]
   |
   | (Step Functions)
   v
[Procesos Automatizados]
```

- **S3 Buckets:** Almacenan los datos fuente y resultados.
- **AWS Glue:** Catalogación automática mediante Crawlers y base Glue.
- **AWS Athena:** Permite consultas SQL serverless sobre los datos.
- **Step Functions:** Orquestación de procesos ETL y consultas automáticas.

---

## 📈 Servicios AWS Utilizados

- Amazon S3
- AWS Glue (Database, Crawler)
- AWS Athena
- AWS Step Functions
- AWS IAM (Roles y Policies)
- AWS CDK (Infraestructura como Código)

---

## 📆 Explicación Detallada

- **Amazon S3:** Contiene los datos crudos y estructurados a analizar.
- **AWS Glue:**
  - **Database:** Define el esquema del catálogo.
  - **Crawler:** Detecta automáticamente estructuras de datos en S3 y actualiza el Glue Catalog.
- **AWS Athena:** Consulta directa de los datos catalogados en S3 mediante SQL.
- **AWS Step Functions:** Orquesta ejecuciones de Glue y Athena según la definición provista (archivo `athenaquery.asl.json`).
- **AWS IAM:** Define roles con permisos específicos para Glue, Step Functions y acceso a buckets S3.

---

## 🌐 Costo Aproximado

| Servicio       | Métrica              | Costo estimado mensual  |
| -------------- | -------------------- | ----------------------- |
| S3             | 10 GB almacenamiento | Bajo (\$0.23 aprox.)    |
| Glue Crawler   | 1 ejecución diaria   | Bajo (\$3-5 aprox.)     |
| Athena         | Consultas moderadas  | Bajo (\$1-5 aprox.)     |
| Step Functions | 1000 ejecuciones/mes | Bajo (\$2-4 aprox.)     |
| **Total**      |                      | **\$10 - \$20 USD/mes** |

> Nota: Estos valores son orientativos y dependen del volumen de datos y frecuencia de consultas.

---

## 📅 Forma de Despliegue

### Prerrequisitos:

- AWS CLI configurado.
- Python 3.7+
- AWS CDK instalado (`npm install -g aws-cdk`).

### Pasos:

```bash
# Clona el repositorio
 git clone https://github.com/arquitectopaul/aws_data_engineering_athena_glue.git
 cd aws_data_engineering_athena_glue

# Crea y activa un entorno virtual
 python -m venv .venv
 source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instala dependencias
 pip install -r requirements.txt

# Sintetiza el stack
 cdk synth

# Despliega en AWS
 cdk deploy
```

---

## 📄 Archivos Relevantes

- `athena_glue_stack.py`: Define la infraestructura completa.
- `requirements.txt`: Define las dependencias Python.
- `athenaquery.asl.json`: Definición de la máquina de estados (Step Functions).

---

## 🌍 Contacto

**Paul Rivera**
AWS Certified Solutions Architect - Associate
