{{- define "digbackend.fullname" -}}
{{- printf "%s-%s" .Release.Name "backend" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "digbackend.selectorLabels" -}}
app: {{ include "digbackend.fullname" . }}
{{- end -}}

{{- define "digbackend.labels" -}}
app.kubernetes.io/name: {{ include "digbackend.fullname" . }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}
