import prometheus_client as pm

USER_REGISTRATIONS = pm.Counter('user_registrations_total', 'Количество регистраций')
USER_AUTHORIZATIONS = pm.Counter('user_authorization_total', 'Количество авторизаций')
PRODUCT_SELL = pm.Counter('product_sold_total', 'Количество проданных товаров')