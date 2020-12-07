<template>
  <q-page>
    <div class="q-pa-md q-col-gutter-sm">
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
              <q-avatar>
                <img src="@/assets/logo_v2.png" alt="Powered by Qdrant" />
              </q-avatar>
            </template>
          </q-input>
        </div>
      </div>
      <div class="row justify-evenly">
        <div class="col-10">
          Try this: <q-chip
            v-for="example in examples"
            v-bind:key="example"
            clickable
            @click="useSample(example)"
            color="secondary"
            text-color="white"
            icon="input"
          >
            {{ example }}
          </q-chip>
        </div>
      </div>
      <div class="row justify-center">
        <div class="col-10">
          <div class="row wrap justify-center q-col-gutter-md" v-if="startups.length > 0">
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
              />
            </div>
          </div>
          <div class="row" v-if="startups.length === 0">
            <div class="col-12 text-grey">
              <h1>Startup Search with <b>Qdrant</b></h1>
              <p :style="{ fontSize: '16pt' }">
                This demo uses a short descriptions of startups to perform a <b>semantic search</b>.
                Each startup description converted into a vector using a pre-trained SentenceTransformer model and uploaded to the Qdrant vector search engine.
                Demo service processes text input with the same model and uses its output to query Qdrant for similar vectors.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <q-page-sticky
      position="bottom-left"
      :offset="[18, 18]"
      class="text-grey"
    >
      <ul>
        <li>
          Data source:
          <a href="https://startups-list.com/">startups-list.com</a>
        </li>
        <li>
          Embedding model: SentenceTransformer
          <code>distilbert-base-nli-stsb-mean-tokens</code> 
          <a href="https://github.com/UKPLab/sentence-transformers"
            > <q-icon name="open_in_new"></q-icon
          ></a>
        </li>
      </ul>
    </q-page-sticky>
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
      if (this.query === '') {
        this.startups = [];
        return;
      }
      axios
        .get("/api/search", { params: { q: this.query } })
        .then((response) => {
          this.startups = response.data.result;
        });
    },
    useSample(sampleText) {
      this.query = sampleText;
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
</style>