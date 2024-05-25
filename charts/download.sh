for ADDON in kiali jaeger prometheus grafana
do
    ADDON_URL="https://raw.githubusercontent.com/istio/istio/release-1.22/samples/addons/$ADDON.yaml"
    mkdir -p istio_addons/$ADDON
    wget -O istio_addons/$ADDON/$ADDON.yaml $ADDON_URL
done