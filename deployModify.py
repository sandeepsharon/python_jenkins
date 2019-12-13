from os import path
import yaml
from kubernetes import client, config



def main():
    # Define the barer token we are going to use to authenticate.
    # See here to create the token:
    # https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/
    aToken = "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tcjZqejYiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjI0Zjc1ZjU2LWVjN2YtNDJkMC04NzgzLTQ3ZTJjMzFmMGZjMyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.PXEBVA_LA1LxE-rbrIp1Zr0yvmwxJn-d18xw3PfXBqZwfrb-fOwCTkseaoBCZMnn0OHjypaQrSA2LPh3p-qaBVnWdV0MRMi8x33fpvcbag2L4inGZC7aGS2TOb411Ltvdt7xXMeLZupPaggJdWFZt3G1I6KV8bbdtds_C5u8XOygBK-um5Xs_vfZ6ub7j6V0NFuwLn1rUiUkLEfQWDx1tI1vLALqimYktX3VKiA6WvQUBYzFHPAAjXddYkFukqtd0yR0qDjSvftT6tPw7gFQ06ls0AvewyLX7ipWZXvVlOR7-Ah4b-_YU0Se3TqSmEMruZ2DgDmX7SkxBMT8VIqEBg"

    # Create a configuration object
    aConfiguration = client.Configuration()

    # Specify the endpoint of your Kube cluster
    aConfiguration.host = "https://192.168.1.57:6443"

    # Security part.
    # In this simple example we are not going to verify the SSL certificate of
    # the remote cluster (for simplicity reason)
    aConfiguration.verify_ssl = False
    # Nevertheless if you want to do it you can with these 2 parameters
    # configuration.verify_ssl=True
    # ssl_ca_cert is the filepath to the file that contains the certificate.
    # configuration.ssl_ca_cert="certificate"

    aConfiguration.api_key = {"authorization": "Bearer " + aToken}

    # Create a ApiClient with our config
    aApiClient = client.ApiClient(aConfiguration)

    # Do calls
    v1 = client.CoreV1Api(aApiClient)
    with open(path.join(path.dirname(__file__), "/root/pod.yml")) as f:
        dep = yaml.safe_load(f)

        v2 = client.AppsV1Api(aApiClient)
        resp = v2.patch_namespaced_deployment(
            body=dep, namespace="default", name=dep.get('metadata').get('name'))
        print("Deployment created. status='%s'" % resp.metadata.name)
    #print("Listing pods with their IPs:")
    #ret = v1.list_pod_for_all_namespaces(watch=False)
    #for i in ret.items:
    #    print("%s\t%s\t%s" %
    #          (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


if __name__ == '__main__':
    main()
