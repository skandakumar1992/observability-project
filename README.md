👉Create a docker and docker-compose in EC2 instance.
⦁	sudo apt update
⦁	sudo apt install ca-certificates curl gnupg -y
⦁	sudo install -m 0755 -d /etc/apt/keyrings
⦁	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
⦁	sudo chmod a+r /etc/apt/keyrings/docker.gpg
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
⦁	sudo apt update
⦁	sudo apt install docker-compose-plugin -y
⦁	sudo usermod -aG docker $USER
⦁	newgrp docker

🚀create a folder 
   mkdir observability 

observability/
├─ docker-compose.yml
├─ prometheus/
│  └─ prometheus.yml
├─ promtail/
│  └─ promtail-config.yml
└─ app/
   ├─ app.py
   ├─ Dockerfile
   └─ requirements.txt

👉For the above tree write a yaml files of docker-compose.yml file,prometheus.yml, promtail-coinfiguration.yml, app.py,requirement.txt, dockerfile 
👉Then ready-to-run docker-compose.yml for a complete observability system with:
   Prometheus → metrics
   Grafana → dashboards
   Loki + Promtail → logs
   Jaeger → tracing
   Sample Python app (Flask) → emits logs + Prometheus metrics
👉docker compose up -d --build
👉docker ps

✅ Test your Flask app
    Run: curl http://<EC2_PUBLIC_IP>:5000/

    we should see:
    Hello, Observability!

✅ Test Prometheus
    Open in browser:
    http://<EC2_PUBLIC_IP>:9090
    Check Status → Targets. You should see your app metrics endpoint (/metrics) being scraped if you configured it in prometheus.yml.

✅ Test Grafana
    Open:http://<EC2_PUBLIC_IP>:3000
    Username: admin
    Password: admin

    Then:
    Add Prometheus datasource → http://prometheus:9090
      In Grafana → Connections → Data sources → Add new datasource
      Select Prometheus
      Set the URL to:http://prometheus:9090
      Click Save & test → it should say “Data source is working”.

    Add Loki datasource → http://loki:3100
      Again, add new datasource.
      Select Loki.
      Set the URL:http://loki:3100
      Save & test.
    
   Add Jaeger datasource → http://jaeger:16686
     Add new datasource.
     Select Jaeger.
     Set the URL:http://jaeger:16686
     Save & test.

✅ Test Jaeger (Tracing)
    Open:http://<EC2_PUBLIC_IP>:16686
    Choose service → flask-app.
    Run queries → you should see spans for your home-request


✅ Test Logs in Loki
    Flask app logs should be written to /var/log/app/app.log inside the container.
    Promtail tails that file and ships to Loki.
    In Grafana → Explore → select Loki datasource → run query:
    {job="flask-app"}
    should see Home endpoint hit messages from your logging.

👉 Verify in Explore
  🔹Switch to Explore in Grafana.
     Choose Prometheus datasource → run query:http_requests_total
     should see metrics when you hit your Flask app.
  🔹Switch to Loki datasource → run query:{job="flask-app"}
     should see logs like “Home endpoint hit”.
  🔹Switch to Jaeger datasource → search for flask-app traces → you should see spans for / requests.


🔜 Next steps (to complete the dashboard you mentioned earlier):
   Add Logs Panel (Loki)
   Go to your dashboard → Add Panel → New Panel
   Choose Loki as the datasource
   Query:{job="flask-app"}
   Visualization → Logs (not Time series).
   Save panel.
   Add Traces Panel (Jaeger)
   Add another panel → Datasource: Jaeger
   Query → select your service (probably flask-app)
   Visualization → Trace or Trace list
   Save panel.

✅ Now your dashboard has:
    Request rate (Prometheus → http_requests_total)
    Logs (Loki → {job="flask-app"})
    Traces (Jaeger → flask-app)
    That completes the Observability Stack (Metrics + Logs + Traces) 🚀.
    Download the save file and export to  json format

👉 create a folder
    mkdir Grafana/dashboard
    move the json file from downloads into dashboard

👉git config --global init.defaultBranch main
 👉git branch -m main
  👉git add.
   👉git init
    👉git remote origin https://github.com/skandakumar1992/observability-project.git
     👉git push-main
