all: clean build push
build:
	cd client && docker build --network=host -t gnes/benchmark:client . && cd -
pull:
	docker pull gnes/gnes:latest-alpine
clean: ; docker stack rm my-gnes
wait: ; @printf "sleep 15s for docker recycling network resources...\n"; sleep 15
client: ; unset https_proxy && unset http_proxy && docker run --rm --network host gnes/benchmark:client --mode index
deploy: ; docker stack deploy --compose-file docker-compose/network1.yml my-gnes

