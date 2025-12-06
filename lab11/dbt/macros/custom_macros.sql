-- macros/custom_macros.sql

{% macro generate_model_name(prefix, suffix) %}
    {{ prefix }}_{{ suffix }}
{% endmacro %}
