# charts/postgresql-chart/templates/_helpers.tpl
{{- define "postgresql-chart.fullname" -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "postgresql-chart.labels" -}}
helm.sh/chart: {{ include "postgresql-chart.chart" . }}
{{ include "postgresql-chart.selectorLabels" . }}
{{- end -}}

{{- define "postgresql-chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "postgresql-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "postgresql-chart.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{- define "postgresql-chart.chart" -}}
{{- .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}
