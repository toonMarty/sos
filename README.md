# SOS
SOS is a help desk ticketing system...

# Elasticsearch installation and Configuration commands

# Step 1 - Installing and Configuring Elasticsearch
```
$ curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elastic.gpg
```

Next, add the Elastic source list to the sources.list.d directory, where apt will search for new sources:

```
$ echo "deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
```
Next, update your package lists so APT will read the new Elastic source:

```
$ sudo apt update
```

Install Elasticsearch with this command:

```
$ sudo apt install elasticsearch
```

# Step 2 - Configuring Elasticsearch
$ sudo vi /etc/elasticsearch/elasticsearch.yml

Upon opening the elasticsearch.yml file, find the line that specifies network.host, uncomment it and replace its value with localhost so it reads like this:

```network.host: localhost
```
Next up, start the elasticsearch service.

Before starting the elasticsearch service, it might help to know which init system you are using so that you can start elasticsearch using the right commands.
To know which init system you are using, use the following command in your terminal:

```
ps -p 1 -o comm=
```
The above command should show **init** or **sysv**. If you see **init**, it means your system is not using systemd and you should use the init command:

| Systemd command (**sysv**)    | Sysvinit command (**init**) |
|-------------------------------|-----------------------------|
| systemctl start elasticsearch | service elasticsearch start |


Next, run the following command to enable Elasticsearch to start up every time your server boots:
Use the appropriate command based on your init system, like in the previous step.

| Systemd command (**sysv**)    | Sysvinit command (**init**)     |
|-------------------------------|---------------------------------|
| systemctl enable elasticsearch| update-rc.d elasticsearch start |


# Step 3 - Securing Elasticsearch

```
$ sudo ufw allow from 198.51.100.0 to any port 9200
```

Check the status of UFW with the following command:

```
$ sudo ufw status
```

If you have specified the rules correctly you should receive output like this:

```
Output
Status: active

To			Action	From
--			------	----
9200			ALLOW	198.51.100.0
22			ALLOW	Anywhere
22 (v6)			ALLOW 	Anywhere (v6)
```
# Step 4 - Testing Elasticsearch
Test that elasticsearch is running using the cURL command and a GET request:

```
$ curl -X GET 'http://localhost:9200'
```

You should receive the response similar to the one shown below:

```
Output
{
  "name" : "elastic-22",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "DEKKt_95QL6HLaqS9OkPdQ",
  "version" : {
    "number" : "7.17.1",
    "build_flavor" : "default",
    "build_type" : "deb",
    "build_hash" : "e5acb99f822233d62d6444ce45a4543dc1c8059a",
    "build_date" : "2022-02-23T22:20:54.153567231Z",
    "build_snapshot" : false,
    "lucene_version" : "8.11.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

For a more detailed description of how to install and configure elasticsearch check out [How To Install and Configure Elasticsearch on Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-22-04)
