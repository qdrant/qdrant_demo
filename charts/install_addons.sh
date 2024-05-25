for ADDON in kiali jaeger prometheus grafana
do
    kubectl apply -f istio_addons/$ADDON
done