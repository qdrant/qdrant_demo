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
import { SearchMode } from "@/api/search";

export function Main() {
  const { classes } = useStyles();
  const [query, setQuery] = useMountedState("");
  const { data, error, loading, getSearch, resetData } = useGetSearchResult();
  const [mode, setMode] = useMountedState<SearchMode>("hybrid");

  const handleSubmit = () => {
    if (query) {
      getSearch(query, mode);
    }
  };

  const onClickFindSimilar = (data: string) => {
    if (data) {
      resetData();
      setQuery(data);
      getSearch(data, mode);
    }
  };

  return (
    <Container className={classes.wrapper} size={1400}>
      <div className={classes.inner}>
        <Title className={classes.title}>
          Startup{" "}
          <Text component="span" className={classes.highlight} inherit>
            Hybrid search
          </Text>{" "}
          with Qdrant
        </Title>
        <Text size="lg" color="dimmed" className={classes.description}>
          Search short descriptions of startups. Switch between semantic,
          keyword, and hybrid to compare how each one ranks.
        </Text>
        <Container p={0} size={600} className={classes.controls}>
          <SegmentedControl
            radius={30}
            data={[
              { label: "Semantic", value: "semantic" },
              { label: "Keyword", value: "keyword" },
              { label: "Hybrid", value: "hybrid" },
            ]}
            onChange={(value) => {
              const next = value as SearchMode;
              setMode(next);
              resetData();
              query && getSearch(query, next);
            }}
            size="md"
            color="Primary.2"
            className={classes.control}
            value={mode}
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
