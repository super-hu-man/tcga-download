curl --request POST --header "Content-Type: application/json" --data @Payload.1.30000 'https://api.gdc.cancer.gov/files' > list.1.30000 & \
curl --request POST --header "Content-Type: application/json" --data @Payload.2.30000 'https://api.gdc.cancer.gov/files' > list.2.30000 & \
curl --request POST --header "Content-Type: application/json" --data @Payload.3.30000 'https://api.gdc.cancer.gov/files' > list.3.30000 & \
curl --request POST --header "Content-Type: application/json" --data @Payload.4.30000 'https://api.gdc.cancer.gov/files' > list.4.30000 & \
curl --request POST --header "Content-Type: application/json" --data @Payload.5.30000 'https://api.gdc.cancer.gov/files' > list.5.30000 &&

awk -F'\t' 'NR==1;FNR>1' list.* > tcga.files.information.txt
