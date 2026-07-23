---
sidebar_position: 80
---

# SCR Publishing Destination

When setting up a publishing destination to deploy to SCR, you need to link the Python library to the publishing destination.
#### Create a Kubernetes ConfigMap File
* Download file [pipConfMap_Neo4j.yaml](https://github.com/sassoftware/sas-id-neo4j-extension/blob/main/data/DNT/publish/pipConfMap_Neo4j.yaml) from Git repository and copy to home directory
* Add ConfigMap file to Kubernetes
    ```
    kubectl apply -f pipConfMap_Neo4j.yaml -n <Viya Namespace>
    ```
#### Create Publishing Destination
From Viya command line create a publishing destination pointing to *pipConfMap_Neo4j*.

**Example:** 
Creating publishing destination pointing to *pip-config-neo4j* and using database *postgresql*.
```
#########################################################
# Set variables for Publishing Destination
#########################################################
PublishingDestination="<Publishing Destination Name>"
RegistryLoginServer="<Container Registry: Login URL>"
RegistryUsername="<Container Registry: Username>"
RegistryPassword="<Container Registry: password>"
ExternalViyaURL="<Viya URL>"

#########################################################
kubeURL="${ExternalViyaURL}:6443"
credDomainID="publishDomain-${PublishingDestination}"

# Create ID publishing destination
sas-viya models destination createPD \
--name "$PublishingDestination" \
--baseRepoURL "$RegistryLoginServer" \
--registryId "$RegistryUsername" \
--registryPassword "$RegistryPassword" \
--kubeURL "$kubeURL" \
--kubeCert "na" \
--kubekey "na" \
--pipConfig pip-config-neo4j \
--databaseDriver postgresql \
--validationNamespace default \
--identityId "SASAdministrators" \
--identityType "group" \
--credDescription "Credentials domain for Container Registry" \
--credDomainID "$credDomainID"

```
ℹ️ **Info:** For more information see [Configure Container Publishing Destinations](https://go.documentation.sas.com/doc/en/sasadmincdc/default/calpubdest/p02scrqf37kexwn1gi60khpshifz.htm#p1f2d2x0t2a3vvn1j88t6ix1f6gm) and [Configure Support for a Private Python Repository](https://go.documentation.sas.com/doc/en/sasadmincdc/default/calpubdest/p02scrqf37kexwn1gi60khpshifz.htm#n1plxwm9hyr84on14yf8bwtgpp1i).
