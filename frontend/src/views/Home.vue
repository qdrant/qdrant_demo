<template>
  <div class="q-pa-md q-col-gutter-sm">
    <div class="row justify-evenly">
      <div class="col-8">
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
              <img src="@/assets/logo_v2.png" alt="Powered by Qdrant"/>
            </q-avatar>
          </template>
        </q-input>
      </div>
    </div>
    <div class="row justify-evenly">
      <div class="col-8">
        <q-chip
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
    <!-- <q-space/> -->
    <div class="row wrap q-col-gutter-md">
      <div class="col-3" v-for="startup in startups" v-bind:key="startup.name">
        <StartupView 
        :name="startup.name"
        :description="startup.description"
        :link="startup.link"
        :image="startup.image"
        :city="startup.city"
        :alt="startup.alt"
        />
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

import StartupView from '@/components/StartupView.vue'

export default {
  name: "Home",
  components: {StartupView},
  data: function () {
    return {
      query: "",
      examples: [
        "smart devices",
        "youtube marketing",
        "online clothes",
        "neural search",
      ],
      startups: [
        {
          name: "Qdrant",
          description: "Vector Similarity Search Engine for semantic search applications \n Advanced filtering support ",
          link: "https://pitch.qdrant.tech",
          image: "/img/spacer.gif",
          city: "Berlin",
          alt: "Vector Search Engine"
        }
      ]
    };
  },
  methods: {
    search() {
      console.log("Search for ", this.query);
    },
    useSample(sampleText) {
      this.query = sampleText;
    },
  },
};
</script>
