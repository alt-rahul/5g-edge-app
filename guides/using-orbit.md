# 5G Edge Cloud Applications

### Setting up nodes:

**Step 1:** To log into sb9:

```bash
#get into folder
cd ./.ssh/
#ssh into orbit sb9
ssh -i .\orbitlab rahulrajkumar@console.sb9.orbit-lab.org 
```

---

**Step 2:**  After logging in, we must now check if what nodes are on or off, to do we can do a stat command:

```bash
#check the status of all nodes
omf stat -t all
```

**Step 3:**  Now that we can see which nodes are off, we must load our image onto a node. But before we can load an image onto a specific node, that node MUST be turned off before hand. So let’s say `node1-4`  was already on. Let’s first turn off the node.

```bash
#turn off specific node (if it says reply: erorr not registered, just do it again)
omf tell -a offh -t node1-4
```

---

**Step 4:**  After the node is turned off, we must load the image. First I’m going to check if my image is there and then load the image on my node. Loading an image typically 9 mins. Here are the steps:

```bash
#checking if my image exists
ls /mnt/images | grep rahul
#(currenly we should be using the image rahulsgoodnode.ndz)
omf load -i rahulsgoodnode.ndz -t node1-4
```

---

**Step 5:**  Once the image has been loaded *successfully* you should turn on the node to use it. However, it would typically take around 4+ mins until you can ssh into the node.

```bash
#turning on the node (if error just doing it again)
omf tell -a on -t node1-4
#ssh into the node but you would have to wait 5 mins after turning on the node
#to be successfully loaded in
ssh root@node1-4
```

### Setting up Grafana & Prometheus:

Now that you have one node set-up, you would need to start running the services, which are `grafana`  and `prometheus` . 

To start `grafana`  we’ll push the following command:

```bash
#start grafana server
sudo systemctl start grafana-server

#to check if it's running
sudo systemctl status grafana-server #and then press q to stop checking
```

Next on the same node, we’ll  start the `prometheus`:

```bash
#go into prometheus folder
cd prometheus
#start the service
./prometheus
```

---

Great, now we have both processes running. Now we need to open two more terminals, one to host each service. In the first terminal, we’ll locally start our `grafana`  service, so do the following:

```bash
# go into ssh folder
cd ./.ssh/
#host the grafana service
ssh -i .\orbitlab -L 3000:10.19.1.1:9100 rahulrajkumar@console.sb9.orbit-lab.org
```

In a new terminal, do something similar:

```bash
# go into ssh folder
cd ./.ssh/
#host the prometheus service
ssh -i .\orbitlab -L 9090:10.19.1.1:9090 rahulrajkumar@console.sb9.orbit-lab.org
```

---

Now go into your browser, and in one tab, go to the following link: [localhost:3000](http://localhost:3000) & and in another go to [localhost:9090](http://localhost:9090). We have now set up grafana and prometheus. 


Made by: [Rahul Rajkumar](https://rajhulrajkumar.vercel.app)