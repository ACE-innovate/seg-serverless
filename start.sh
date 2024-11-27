# Start the segmentation server in the background
echo "Starting segmentation server (8083)..."
(bash -c "cd /seg && python3 server.py") > /seg.log &

# Start the Runpod handler
echo "Starting Runpod handler..."
(bash -c "python3 /handler.py > /handler.log") &&

tail -f /seg.log 