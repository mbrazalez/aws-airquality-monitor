El objetivo de este proyecto será crear una arquitectura en AWS capaz de recolectar información relacionada con la calidad del aire a través del uso de web scraping. Para ello, utilizaremos la página web [troposfera.es](https://troposfera.es/datos/dev-albacete/#/dashboard) como fuente de datos. En base a los datos recopilados, podremos monitorizar la calidad del aire en la ciudad de Albacete con el objetivo de estudiar la calidad del aire en tiempo real y poder tomar decisiones en base a esta información.

![AWS Architecture here](https://github.com/mbrazalez/aws-airquality-monitior/blob/main/diagrama.png)

- **Paso 1:** Definiremos cada cuánto queremos que se ejecute la lambda que se encargará del web scraping usando un schedule event.
- **Paso 2:** Utilizaremos el servicio de AWS EventBridge con el schedule previamente configurado, para programar la ejecución de la función lambda que contiene el código para realizar el web scraping que se encargará de recopilar los datos de la página web mencionada anteriormente.
- **Paso 3:** Los datos recopilados se almacenarán en una base de datos NoSQL de AWS DynamoDB.
- **Paso 4:** Con la ayuda del servicio de AWS QuickSight podremos ofrecer a un usuario los datos almacenados en DynamoDB de una forma visual y sencilla.
- **Paso 5:** Al añadir un nuevo dato a la base de datos, se disparará una lambda encargada de enviar una notificación a un usuario a través del servicio de mensajería SNS.
- **Paso 6:** La función lambda se encarga de enviar la notificación al tópico de SNS, para que los usuarios suscritos reciban un email indicando que se ha almacenado en la base de datos nueva información relacionada con la calidad del aire.

