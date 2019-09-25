all: clean build push
build:
	cd client && docker build --network=host -t gnes/benchmark:client . && cd -
pull:
	docker pull gnes/gnes:latest-alpine
clean: ; rm -rf .data && mkdir -p .data && docker stack rm my-gnes
wait: ; @printf "sleep 10s for docker recycling network resources...\n" && sleep 10
run_client: ; unset https_proxy && unset http_proxy && docker run --rm --network host -v $(PWD)/.data:/workspace gnes/benchmark:client --mode index --num_bytes $(s) --num_docs $(d) --batch_size $(b) --test_id $(id) --override_benchmark
run_server: ; docker stack deploy --compose-file docker-compose/network$(id).yml my-gnes
test: clean run_server run_client

