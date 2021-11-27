#!/usr/bin/env python
from constructs import Construct
from cdk8s import App, Chart
from imports import k8s


class MyChart(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # define resources here
        label = {"app": "hello-k8s"}
        
        # notice that there is no assigment neccesary when creating resources.
        # simply instantiating the resource is enough because it adds it to the construct tree via
        # the first argument, which is always the parent construct.
        # its a little confusing at first glance, but this is an inherent aspect of the constructs
        # programming model, and you will encounter it many times.
        # you can still perform an assignment of course, if you need to access
        # atrtibutes of the resource in other parts of the code.

        k8s.KubeService(self, 'service',
                    spec=k8s.ServiceSpec(
                    type='LoadBalancer',
                    ports=[k8s.ServicePort(port=80, target_port=k8s.IntOrString.from_number(8080))],
                    selector=label))

        k8s.KubeDeployment(self, 'deployment',
                    spec=k8s.DeploymentSpec(
                        replicas=2,
                        selector=k8s.LabelSelector(match_labels=label),
                        template=k8s.PodTemplateSpec(
                        metadata=k8s.ObjectMeta(labels=label),
                        spec=k8s.PodSpec(containers=[
                            k8s.Container(
                            name='hello-kubernetes',
                            image='paulbouwer/hello-kubernetes:1.7',
                            ports=[k8s.ContainerPort(container_port=8080)])]))))


        k8s.KubeDeployment(self, 'mydeployment',
                            spec=k8s.DeploymentSpec(
                                selector=k8s.LabelSelector(), 
                                template=k8s.PodTemplateSpec( 
                                    metadata=k8s.ObjectMeta(), 
                                    spec=k8s.PodSpec(containers=k8s.Sequence[k8s.Container(
                                                            name=k8s.str(), 
                                                            args=k8s.Sequence[str] | None = None, 
                                                            command=k8s.Sequence[str] | None = None, 
                                                            env=k8s.Sequence[EnvVar()] | None = None, 
                                                            env_from=k8s.Sequence[EnvFromSource] | None = None, 
                                                            image=k8s.str() | None = None, 
                                                            image_pull_policy: str | None = None, 
                                                            lifecycle: Lifecycle | None = None, 
                                                            liveness_probe: Probe | None = None, 
                                                            ports: Sequence[ContainerPort] | None = None, 
                                                            readiness_probe: Probe | None = None, 
                                                            resources: ResourceRequirements | None = None, 
                                                            security_context: SecurityContext | None = None, 
                                                            startup_probe=k8s.Probe() | None = None, 
                                                            stdin: bool | None = None, 
                                                            stdin_once: bool | None = None, 
                                                            termination_message_path: str | None = None, 
                                                            termination_message_policy: str | None = None, 
                                                            tty: bool | None = None, 
                                                            volume_devices: Sequence[VolumeDevice] | None = None, 
                                                            volume_mounts: Sequence[VolumeMount] | None = None, 
                                                            working_dir: str | None = None)
                                                            )], 
                                                    active_deadline_seconds=k8s.Any | None = None, 
                                                    affinity: Affinity | None = None, 
                                                    automount_service_account_token: bool | None = None, 
                                                    dns_config: PodDnsConfig | None = None, 
                                                    dns_policy: str | None = None, 
                                                    enable_service_links: bool | None = None, 
                                                    ephemeral_containers: Sequence[EphemeralContainer] | None = None, 
                                                    host_aliases: Sequence[HostAlias] | None = None, 
                                                    host_ipc: bool | None = None, 
                                                    hostname: str | None = None, 
                                                    host_network: bool | None = None, 
                                                    host_pid: bool | None = None, 
                                                    image_pull_secrets: Sequence[LocalObjectReference] | None = None, 
                                                    init_containers: Sequence[Container] | None = None, 
                                                    node_name: str | None = None, 
                                                    node_selector: Mapping[str, str] | None = None, 
                                                    overhead: Mapping[str, Quantity] | None = None, 
                                                    preemption_policy: str | None = None, 
                                                    priority: Any | None = None, 
                                                    priority_class_name: str | None = None, 
                                                    readiness_gates: Sequence[PodReadinessGate] | None = None, 
                                                    restart_policy: str | None = None, 
                                                    runtime_class_name: str | None = None, 
                                                    scheduler_name: str | None = None, 
                                                    security_context: PodSecurityContext | None = None, 
                                                    service_account: str | None = None, 
                                                    service_account_name: str | None = None, 
                                                    set_hostname_as_fqdn: bool | None = None, 
                                                    share_process_namespace: bool | None = None, 
                                                    subdomain: str | None = None, 
                                                    termination_grace_period_seconds: Any | None = None, 
                                                    tolerations: Sequence[Toleration] | None = None, 
                                                    topology_spread_constraints: Sequence[TopologySpreadConstraint] | None = None, 
                                                    volumes: Sequence[Volume] | None = None)), 
                                min_ready_seconds=k8s.Any(), 
                                paused=k8s.bool(), 
                                progress_deadline_seconds=k8s.Any(), 
                                replicas=k8s.Any(), 
                                revision_history_limit=k8s.Any(), 
                                strategy=k8s.DeploymentStrategy("RollingUpdate")))

app = App()
MyChart(app, "CDK8s-Kubernetes-with-Python")

app.synth()

print(help(k8s.KubeDeployment()))