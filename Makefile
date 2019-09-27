all: clean build push
build:
	cd client && docker build --network=host --build-arg GNES_IMG_TAG=$(GNES_IMG_TAG) -t gnes/benchmark:client . && cd -
pull:
	docker pull gnes/gnes:$(GNES_IMG_TAG)
clean: ; rm -rf .data/network*.json && mkdir -p .data && docker stack rm my-gnes
wait: ; @printf "sleep $(t)s for docker recycling network resources...\n" && sleep $(t)
run_client: ; unset https_proxy && unset http_proxy && docker run --rm --network host --env GNES_BENCHMARK_ID=$(GNES_BENCHMARK_ID) --env GNES_IMG_TAG=$(GNES_IMG_TAG) --env BENCHMARK_DIR=$(BENCHMARK_DIR) -v $(SHARED_HOST_PATH):/workspace gnes/benchmark:client --mode index --num_bytes $(s) --num_docs $(d) --batch_size $(b)
run_server: ; docker stack deploy --compose-file docker-compose/network$(GNES_BENCHMARK_ID).yml my-gnes
test: clean run_server run_client

