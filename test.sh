npm install 

port activate openssl @1.1_3
port uninstall python39
port clean python39
port install -s -f python39

# Copy data directory to a temporary directory
cp -r ./data ./tmp-data

# Spawn Bitcoind, and provide execution permission.
docker compose up -d

# wait for esplora to be ready
for i in {1..24}; do
  curl --fail -X GET http://localhost:8094/regtest/api/blocks/tip/height && break || sleep 1
done

chmod +x ./bash/run-bash.sh
chmod +x ./python/run-python.sh
chmod +x ./javascript/run-javascript.sh
chmod +x ./rust/run-rust.sh
chmod +x ./run.sh

# Run the test scripts
/bin/bash run.sh
npm run test
docker compose down -v

# Remove the temporary directory
rm -rf ./tmp-data