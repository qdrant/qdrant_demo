<template>
  <q-page>
    <div class="q-pa-md q-col-gutter-sm items-stretch">
      <div class="row justify-evenly">
        <div class="col-10">
          <q-input
            outlined
            v-model="query"
            placeholder="Search"
            color="black"
            :input-style="{ fontSize: '16pt' }"
            v-on:keyup.enter="search"
          >
            <template v-slot:append>
              <div v-if="neural">
                Neural
                <q-avatar style='width: auto;'>
                  <img src="@/assets/logo_v3.png" alt="Powered by Qdrant"/>
                </q-avatar>
              </div>
              <div v-if="!neural">Text</div>
              <q-toggle v-model="neural" @input="search" color="pink-9"/>
            </template>
          </q-input>
        </div>
      </div>
      <div class="row justify-evenly">
        <div class="col-10">
          Try this:
          <q-chip
            v-for="example in examples"
            v-bind:key="example"
            clickable
            @click="useSample(example)"
            color="brand-secondary"
            text-color="white"
            icon="input"
          >
            {{ example }}
          </q-chip>
        </div>
      </div>
      <div class="row justify-center">
        <div class="col-10">
          <div
            class="row wrap justify-center q-col-gutter-md"
            v-if="startups.length > 0"
          >
            <div
              class="col-4"
              v-for="startup in startups"
              v-bind:key="startup.name"
            >
              <StartupView
                :name="startup.name"
                :description="startup.description"
                :link="startup.link"
                :images="startup.images"
                :city="startup.city"
                :alt="startup.alt"
                @select="findSimilar(startup)"
              />
            </div>
          </div>
          <div class="row" v-if="startups.length === 0">
            <div class="col-12 text-grey">
              <h1>Startup Search with <b>Qdrant</b></h1>
              <p :style="{ fontSize: '16pt' }">
                This demo uses short descriptions of startups to perform a
                <b>semantic search</b>. Each startup description converted into
                a vector using a <b>pre-trained</b> SentenceTransformer model
                and uploaded to the Qdrant vector search engine. Demo service
                processes text input with the same model and uses its output to
                query Qdrant for similar vectors.
              </p>
              <p :style="{ fontSize: '16pt' }">
                You can turn neural search on and off to compare the result with
                regular full-text search. Try to use startup description to find
                similar ones.
              </p>
              <p :style="{ fontSize: '16pt' }">
                You will discover that given a <b>short query</b> - a full-text
                search provides more precise results but lower recall when a
                neural search may find close and fuzzy matches. For
                <b>similarity search and longer queries</b> - full-text search
                struggles to catch the meaning of the query and return noisy
                results, while neural search finds better and semantically
                closer results.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <q-footer class="bg-white text-grey q-ml-md">
      <ul>
        <li>
          Data source:
          <a href="https://startups-list.com/">startups-list.com</a>
        </li>
        <li>
          Embedding model: SentenceTransformer
          <code>distilbert-base-nli-stsb-mean-tokens</code>
          <a href="https://github.com/UKPLab/sentence-transformers">
            <q-icon name="open_in_new"></q-icon
          ></a>
        </li>
      </ul>
    </q-footer>
  </q-page>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
import StartupView from "@/components/StartupView.vue";

export default {
  name: "Home",
  components: { StartupView },
  data: function () {
    return {
      neural: true,
      query: "",
      examples: [
        "smart devices",
        "youtube marketing",
        "online clothes",
        "neural search",
        "cyber sport",
        "connect jobs and employers",
      ],
      startups: [
        // {
        //   name: "Qdrant",
        //   description:
        //     "Vector Similarity Search Engine for semantic search applications \n Advanced filtering support ",
        //   link: "https://pitch.qdrant.tech",
        //   images: "/img/spacer.gif",
        //   city: "Berlin",
        //   alt: "Vector Search Engine",
        // },
      ],
    };
  },
  methods: {
    search() {
      if (this.query === "") {
        this.startups = [];
        return;
      }
      axios
        .get("/api/search", { params: { q: this.query, neural: this.neural } })
        .then((response) => {
          this.startups = response.data.result;
        });
    },
    useSample(sampleText) {
      this.query = sampleText;
      this.search();
    },
    findSimilar(startup) {
      this.query = startup.description
        .replaceAll("<b>", "")
        .replaceAll("</b>", "")
        .replaceAll("\n", " ");
      this.neural = true;
      this.search();
    },
  },
};
</script>

<style scoped>
ul {
  list-style-type: none;
  /*use padding to move list item from left to right*/
  padding-left: 1em;
}

ul li:before {
  content: "–";
  position: absolute;
  margin-left: -1em;
}

.bg-brand-secondary {
  background: #bc1439;
}

.text-bg-secondary {
  color: #bc1439;
}

</style>