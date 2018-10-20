url=${URLS}
apikey=XXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
timestamp=$(date +"%m-%d-%y")

while read -r line
do 

if [ ! -z "$url" ]
then
uuid=$(curl -X POST "https://urlscan.io/api/v1/scan/" -H "Content-Type: application/json" -H "API-Key:$apikey" -d "{\"url\": \"$url\", \"public\": \"on\"}" | jq '.uuid' | tr -d '"')
sleep 2m;

mkdir -p /var/log/urlscanio
wait
curl https://urlscan.io/api/v1/result/$uuid/ | tr -d '\r\n' >> /var/log/urlscanio/$uuid-"$timestamp".json
wait
curl https://urlscan.io/screenshots/$uuid.png >> /var/log/urlscanio/$uuid-"$timestamp".png
wait
curl https://urlscan.io/dom/$uuid/  >> /var/log/urlscanio/$uuid-"$timestamp".dom
wait
jq '.data.requests[] | [ .response.response.url, .response.response.status, .response.response.statusText, .response.response.headers.Server, .response.response.mimeType, .response.response.remoteIPAddress, .response.response.remotePort, .response.response.encodedDataLength, .response.response.protocol, .response.hash, .response.size, .response.asn.ip, .response.asn.asn, .response.asn.country, .response.asn.registrar, .response.asn.date, .response.geoip.country, .response.geoip.city, .response.geoip.country_name, .response.rdns.ptr]' /var/log/urlscanio/$uuid-"$timestamp".json | tr -d '\r\n' | sed 's/\]\[/\r\n/g' | tr -d ']' | tr -d '[' | sed 's/  //' >> /var/log/urlscanio/$uuid-"$timestamp".csv
wait
fi
done <<<"${URLS}"
