import {
  Title,
  Text,
  Button,
  Container,
  TextInput,
  Loader,
  Box,
  Grid,
  Image,
  SegmentedControl,
} from "@mantine/core";
import { IconSearch } from "@tabler/icons-react";
import { useStyles } from "./style";
import useMountedState from "@/hooks/useMountedState";
import { useGetSearchResult } from "@/hooks/useGetSearchResult";
import { getHotkeyHandler } from "@mantine/hooks";
import { StartupCard } from "../StartupCard";
import DemoSearch from "../DemoSearch";

export function Main() {
  const { classes } = useStyles();
  const [query, setQuery] = useMountedState("");
  const { data, error, loading, getSearch, resetData } = useGetSearchResult();
  const [isNeural, setIsNeural] = useMountedState(true);

  const handleSubmit = () => {
    if (query) {
      getSearch(query, isNeural);
    }
  };

  const onClickFindSimilar = (data: string) => {
    if (data) {
      resetData();
      setQuery(data);
      getSearch(data, isNeural);
    }
  };

  return (
    <Container className={classes.wrapper} size={1400}>
      <div className={classes.inner}>
        <Title className={classes.title}>
          Startup{" "}
          <Text component="span" className={classes.highlight} inherit>
            Semantic search
          </Text>{" "}
          with Qdrant
        </Title>
        <Text size="lg" color="dimmed" className={classes.description}>
          This demo uses short descriptions of startups to perform a semantic
          search.
        </Text>
        <Container p={0} size={600} className={classes.controls}>
          <SegmentedControl
            radius={30}
            data={[
              { label: "Neural", value: "neural" },
              { label: "Text", value: "text" },
            ]}
            onChange={(value) => {
              setIsNeural(value === "neural");
              resetData();
              query && getSearch(query, value === "neural");
            }}
            size="md"
            color="Primary.2"
            className={classes.control}
            value={isNeural ? "neural" : "text"}
          />
          <TextInput
            radius={30}
            size="md"
            icon={<IconSearch color="#102252" />}
            placeholder="Enter a query"
            rightSection={
              <Button
                className={classes.inputRightSection}
                radius={30}
                size={"md"}
                variant="filled"
                color="Primary.2"
                onClick={handleSubmit}
              >
                Search
              </Button>
            }
            rightSectionWidth={"6rem"}
            className={classes.inputArea}
            value={query}
            required
            onChange={(event) => setQuery(event.currentTarget.value)}
            onKeyDown={getHotkeyHandler([["Enter", handleSubmit]])}
          />
        </Container>

        <DemoSearch handleDemoSearch={onClickFindSimilar} />
        <Container className={classes.viewResult}>
          {loading ? (
            <Box
              sx={{
                display: "flex",
                justifyContent: "center",
              }}
            >
              <Loader size="xl" color="Primary.2" variant="bars" />
            </Box>
          ) : error ? (
            <Box
              sx={{
                width: "100%",
                display: "flex",
                justifyContent: "center",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              <Image maw={240} src="./error.gif" alt="No results found." />

              <Text size="lg" color="dimmed" className={classes.description}>
                Error: {error}
              </Text>
            </Box>
          ) : data?.result ? (
            <Grid mt={"md"}>
              {data.result.length > 0 ? (
                data.result.map((item) => (
                  <Grid.Col span={12} key={item.uuid}>
                    <StartupCard
                      name={item.name}
                      images={item.logo_url}
                      alt={item.name}
                      description={item.document}
                      link={item.homepage_url}
                      city={
                        item.city ??
                        item.region ??
                        item.country_code ??
                        "Unknown"
                      }
                      onClickFindSimilar={onClickFindSimilar}
                      Index={item.uuid}
                    />
                  </Grid.Col>
                ))
              ) : (
                <Box
                  sx={{
                    width: "100%",
                    display: "flex",
                    justifyContent: "center",
                    flexDirection: "column",
                    alignItems: "center",
                  }}
                >
                  <Image
                    maw={240}
                    src="./NoResult.gif"
                    alt="No results found."
                  />

                  <Text
                    size="lg"
                    color="dimmed"
                    className={classes.description}
                  >
                    No results found. Try to use another query.
                  </Text>
                </Box>
              )}
            </Grid>
          ) : (
            <Box
              sx={{
                width: "100%",
                display: "flex",
                justifyContent: "center",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              <Image maw={240} src="./home.gif" alt="No results found." />

              <Text size="lg" color="dimmed" className={classes.description}>
                Enter a query to start searching.
              </Text>
            </Box>
          )}
        </Container>
      </div>
    </Container>
  );
}
