curl 'https://x0o1h31a99-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.4.0)%3B%20Browser%20(lite)%3B%20JS%20Helper%20(3.5.5)%3B%20react%20(17.0.2)%3B%20react-instantsearch%20(6.12.1)&x-algolia-api-key=Y2VhMDcxZTk3MGI2YTQxZTQ2MDQ3ZWYzNWViYjA4MWZkMjQ1NjNmNzlmYjkxMmFmYjA0ZjA0MjA0NDNhMmE0NnJlc3RyaWN0SW5kaWNlcz0lNUIlMjJBdmVuZ2VyX0NvbXBhbnlfcHJvZHVjdGlvbiUyMiU1RCZmaWx0ZXJzPXRyYWNrcy53czIxJTNBQUxQSEErT1IrdHJhY2tzLndzMjElM0FCRVRBK09SK3RyYWNrcy53czIxJTNBR1JPV1RI&x-algolia-application-id=X0O1H31A99' \
  -H 'Connection: keep-alive' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -H 'Accept: */*' \
  -H 'Sec-GPC: 1' \
  -H 'Origin: https://websummit.com' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://websummit.com/' \
  -H 'Accept-Language: en-US,en;q=0.9,ru;q=0.8' \
  --data-raw '{"requests":[{"indexName":"Avenger_Company_production","params":"highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&hitsPerPage=1000&tagFilters=%5B%22ws21%22%5D&query=&maxValuesPerFacet=100&page=0&facets=%5B%22country%22%2C%22industries.ws21%22%5D"}]}' \
  --compressed | jq > data/web_summit_startups_raw.json

cat data/web_summit_startups_raw.json | jq -c '.results[0].hits[] | {
    name: .name,
    logo: .logo_urls.original,
    city: .city,
    country: .country,
    homepage: .external_urls.homepage,
    industry: .industries.ws21,
    description: .elevator_pitch
}' > data/web_summit_startups.jsonl

curl 'https://x0o1h31a99-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.4.0)%3B%20Browser%20(lite)%3B%20JS%20Helper%20(3.5.5)%3B%20react%20(17.0.2)%3B%20react-instantsearch%20(6.12.1)&x-algolia-api-key=Y2VhMDcxZTk3MGI2YTQxZTQ2MDQ3ZWYzNWViYjA4MWZkMjQ1NjNmNzlmYjkxMmFmYjA0ZjA0MjA0NDNhMmE0NnJlc3RyaWN0SW5kaWNlcz0lNUIlMjJBdmVuZ2VyX0NvbXBhbnlfcHJvZHVjdGlvbiUyMiU1RCZmaWx0ZXJzPXRyYWNrcy53czIxJTNBQUxQSEErT1IrdHJhY2tzLndzMjElM0FCRVRBK09SK3RyYWNrcy53czIxJTNBR1JPV1RI&x-algolia-application-id=X0O1H31A99' \
  -H 'Connection: keep-alive' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -H 'Accept: */*' \
  -H 'Sec-GPC: 1' \
  -H 'Origin: https://websummit.com' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://websummit.com/' \
  -H 'Accept-Language: en-US,en;q=0.9,ru;q=0.8' \
  --data-raw '{"requests":[{"indexName":"Avenger_Company_production","params":"highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&hitsPerPage=1000&tagFilters=%5B%22ws21%22%5D&query=&maxValuesPerFacet=100&page=1&facets=%5B%22country%22%2C%22industries.ws21%22%5D"}]}' \
  --compressed | jq > data/web_summit_startups_raw_p2.json


cat data/web_summit_startups_raw_p2.json | jq -c '.results[0].hits[] | {
    name: .name,
    logo: .logo_urls.original,
    city: .city,
    country: .country,
    homepage: .external_urls.homepage,
    industry: .industries.ws21,
    description: .elevator_pitch
}' >> data/web_summit_startups.jsonl