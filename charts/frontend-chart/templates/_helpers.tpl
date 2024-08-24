{{- define "digfrontend.fullname" -}}
{{- printf "%s-%s" .Release.Name "frontend" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "digfrontend.selectorLabels" -}}
app: {{ include "digfrontend.fullname" . }}
{{- end -}}

{{- define "digfrontend.labels" -}}
app.kubernetes.io/name: {{ include "digfrontend.fullname" . }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}
