FROM node:18.17.1

WORKDIR /usr/src/star-burger

COPY . .

RUN npm ci --dev
#CMD [ "./node_modules/.bin/parcel", "build", "bundles-src/index.js", "--dist-dir", "bundles", "--public-url=\"./\"" ]
RUN ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
