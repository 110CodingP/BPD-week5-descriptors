cp -r ./data ./tmp-data
docker compose up -d

# wait for esplora to be ready
for i in {1..24}; do
  curl --fail -X GET http://localhost:8094/regtest/api/blocks/tip/height && break || sleep 1
done
