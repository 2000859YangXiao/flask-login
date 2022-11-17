FROM nginx:1.15.8

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

RUN pip3 install --no-cache-dir -r requirements.txt 
CMD flask run --host=0.0.0.0
