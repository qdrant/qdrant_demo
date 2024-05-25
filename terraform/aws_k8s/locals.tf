# Ports needed to correctly install Istio for the error message: transport: Error while dialing dial tcp xx.xx.xx.xx15012: i/o timeout
locals {
  istio_ports = [
    {
      description = "Envoy admin port / outbound"
      from_port   = 15000
      to_port     = 15001
    },
    {
      description = "Debug port"
      from_port   = 15004
      to_port     = 15004
    },
    {
      description = "Envoy inbound"
      from_port   = 15006
      to_port     = 15006
    },
    {
      description = "HBONE mTLS tunnel port / secure networks XDS and CA services (Plaintext)"
      from_port   = 15008
      to_port     = 15010
    },
    {
      description = "XDS and CA services (TLS and mTLS)"
      from_port   = 15012
      to_port     = 15012
    },
    {
      description = "Control plane monitoring"
      from_port   = 15014
      to_port     = 15014
    },
    {
      description = "Webhook container port, forwarded from 443"
      from_port   = 15017
      to_port     = 15017
    },
    {
      description = "Merged Prometheus telemetry from Istio agent, Envoy, and application, Health checks"
      from_port   = 15020
      to_port     = 15021
    },
    {
      description = "DNS port"
      from_port   = 15053
      to_port     = 15053
    },
    {
      description = "Envoy Prometheus telemetry"
      from_port   = 15090
      to_port     = 15090
    },
    {
      description = "aws-load-balancer-controller"
      from_port   = 9443
      to_port     = 9443
    }
  ]

  ingress_rules = {
    for ikey, ivalue in local.istio_ports :
    "${ikey}_ingress" => {
      description = ivalue.description
      protocol    = "tcp"
      from_port   = ivalue.from_port
      to_port     = ivalue.to_port
      type        = "ingress"
      self        = true
    }
  }

  egress_rules = {
    for ekey, evalue in local.istio_ports :
    "${ekey}_egress" => {
      description = evalue.description
      protocol    = "tcp"
      from_port   = evalue.from_port
      to_port     = evalue.to_port
      type        = "egress"
      self        = true
    }
  }
}