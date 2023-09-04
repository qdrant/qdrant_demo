import {
  Title,
  Text,
  Button,
  Container,
  TextInput,
  Loader,
  Switch,
  Box,
  Grid,
  ActionIcon,
  Image,
  Modal,
} from "@mantine/core";
import { IconSearch, IconX } from "@tabler/icons-react";
import { useStyles } from "./style";
import useMountedState from "@/hooks/useMountedState";
import { useGetSearchResult } from "@/hooks/useGetSearchResult";
import { getHotkeyHandler, useDisclosure } from "@mantine/hooks";
import { StartupCard } from "../StartupCard";

export function Main() {
  const { classes } = useStyles();
  const [query, setQuery] = useMountedState("");
  const { data, error, loading, getSearch, resetData } = useGetSearchResult();
  const [isNeural, setIsNeural] = useMountedState(true);
  const [opened, { open, close }] = useDisclosure(false);

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

        <Container p={0} size={600}>
          <Text size="lg" color="dimmed" className={classes.description}>
            This demo uses short descriptions of startups to perform a semantic
            search.
          </Text>
        </Container>

        <Container p={0} size={600} mt={30}>
          <TextInput
            icon={<IconSearch />}
            placeholder="Enter a query"
            rightSection={
              <Box className={classes.inputRightSection}>
                {loading && <Loader size="xs" color="Primary.2" />}
                {query && (
                  <ActionIcon
                    onClick={() => {
                      setQuery("");
                      resetData();
                    }}
                    color="Primary.2"
                    sx={{
                      cursor: "pointer",
                    }}
                  >
                    <IconX size="1.1rem" stroke={1.5} />
                  </ActionIcon>
                )}
                {isNeural ? (
                  <Text color="Primary.2">Neural</Text>
                ) : (
                  <Text>Text</Text>
                )}
                <Switch
                  checked={isNeural}
                  onChange={(event) => {
                    setIsNeural(event.currentTarget.checked);
                    resetData();
                    query && getSearch(query, event.currentTarget.checked);
                  }}
                  color="Primary.2"
                />
              </Box>
            }
            className={classes.inputArea}
            value={query}
            onChange={(event) => setQuery(event.currentTarget.value)}
            onKeyDown={getHotkeyHandler([["Enter", handleSubmit]])}
          />
          <Box className={classes.controls}>
            <Button
              className={classes.control}
              size="md"
              color="Primary.2"
              disabled={loading}
              onClick={handleSubmit}
              rightIcon={loading && <Loader size="xs" color="white" />}
            >
              Search
            </Button>
            <Button
              className={classes.control}
              size="md"
              variant="default"
              onClick={open}
            >
              How it works?
            </Button>
          </Box>
        </Container>
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
            <Grid>
              {data.result.length > 0 ? (
                data.result.map((item) => (
                  <Grid.Col md={6} lg={4} key={item.Index}>
                    <StartupCard
                      data={item}
                      onClickFindSimilar={onClickFindSimilar}
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

      <Modal opened={opened} onClose={close} title="How it works?" centered>
        <Modal.Body>
          <Text size="lg" color="dimmed" className={classes.description}>
            This demo uses short descriptions of startups to perform a semantic
            search. Each startup description converted into a vector using a
            pre-trained SentenceTransformer model and uploaded to the Qdrant
            vector search engine.
          </Text>
          <Text size="lg" color="dimmed" className={classes.description}>
            You can turn neural search on and off to compare the result with
            regular full-text search. Try to use startup description to find
            similar ones.
          </Text>
          <Text size="lg" color="dimmed" className={classes.description}>
            You will discover that given a short query - a full-text search
            provides more precise results but lower recall when a neural search
            may find close and fuzzy matches. For similarity search and longer
            queries - full-text search struggles to catch the meaning of the
            query and return noisy results, while neural search finds better and
            semantically closer results.
          </Text>
        </Modal.Body>
      </Modal>
    </Container>
  );
}
