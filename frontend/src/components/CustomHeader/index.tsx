import {
  createStyles,
  Header as MantineHeader,
  Group,
  ActionIcon,
  Container,
  rem,
  Tooltip,
  Button,
  Modal,
  Text,
  Title,
  Image,
} from "@mantine/core";
import { IconBrandGithub, IconBook2 } from "@tabler/icons-react";
import { Logo } from "../Logo";
import { useDisclosure } from "@mantine/hooks";

const useStyles = createStyles((theme) => ({
  inner: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    height: rem(56),

    [theme.fn.smallerThan("sm")]: {
      justifyContent: "flex-start",
    },
  },

  links: {
    width: rem(260),
    [theme.fn.smallerThan("sm")]: {
      width: "auto",
      marginLeft: "auto",
    },
  },
  link: {
    transition: "transform .3s ease-in-out",
    "&:hover ": {
      transform: "scale(1.3)",
    },
  },
  modalBtn: {
    textAlign: "center",
    fontFamily: "Roboto",
    fontSize: "1rem",
    fontStyle: "normal",
    fontWeight: 400,
    lineHeight: "1rem",
    textDecorationLine: "underline",
  },
  description: {
    ":not(:first-of-type)": {
      paddingTop: "1rem",
    },
    paddingBottom: "1rem",
    textAlign: "center",
    color: theme.colors.Neutral[6],
    fontSize: theme.other.paragraph.sizes.P14.fontSize,
    lineHeight: theme.other.paragraph.sizes.P14.lineHeight,
    fontWeight: theme.other.paragraph.sizes.P14.fontWeight,
  },
  modalHeader: {
    color: theme.colors.Neutral[8],
    fontSize: "2rem",
    fontWeight: 700,
    lineHeight: "2.5rem",
    letterSpacing: "0em",
    textAlign: "center",
    width: "100%",
  },
  highlight: {
    color: theme.colors[theme.primaryColor][2],
  },
  subHeading: {
    fontSize: "1.125rem",
    fontWeight: 600,
    lineHeight: "1.6875rem",
    letterSpacing: "0em",
    textAlign: "center",
    width: "100%",
    paddingTop: "1rem",
    color: theme.colors.Neutral[8],
  },
  modalBtnInner: {
    width: "200px",
    marginTop: "2rem",
  },
}));

export function CustomHeader() {
  const { classes } = useStyles();
  const [opened, { open, close }] = useDisclosure(false);

  return (
    <MantineHeader
      height={56}
      bg={"Neutral.0"}
      fixed
      sx={{
        zIndex: 100,
      }}
    >
      <Container className={classes.inner}>
        <Logo size={35} />

        <Group spacing={10} className={classes.links} position="right" noWrap>
          <Button
            color="Neutral.6"
            variant="subtle"
            className={classes.modalBtn}
            onClick={open}
          >
            How it works?
          </Button>

          <Tooltip label="View Code" position="bottom" withArrow>
            <ActionIcon
              size="lg"
              radius="xs"
              color="Neutral.8"
              variant="filled"
              component="a"
              href="https://github.com/qdrant/qdrant_demo"
              target="_blank"
              className={classes.link}
            >
              <IconBrandGithub size="1.1rem" stroke={1.5} />
            </ActionIcon>
          </Tooltip>
          <Tooltip label="View Docs" position="bottom" withArrow>
            <ActionIcon
              size="lg"
              radius="xs"
              color="Neutral.8"
              variant="filled"
              component="a"
              href="https://github.com/qdrant/qdrant_demo/blob/master/README.md"
              target="_blank"
              className={classes.link}
            >
              <IconBook2 size="1.1rem" stroke={1.5} />
            </ActionIcon>
          </Tooltip>
        </Group>
      </Container>
      <Modal opened={opened} onClose={close} centered size={"lg"}>
        <Modal.Header
          sx={{
            flexDirection: "column",
          }}
        >
          <Title className={classes.modalHeader}>
            How does{" "}
            <Text component="span" className={classes.highlight} inherit>
              Semantic search
            </Text>{" "}
            work?
          </Title>
          <Text className={classes.subHeading}>
            This demo uses short descriptions of startups to perform a semantic
            search.
          </Text>
        </Modal.Header>
        <Modal.Body
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Text size="lg" color="dimmed" className={classes.description}>
            Each startup description is converted into a vector using a
            pre-trained SentenceTransformer model and uploaded to the Qdrant
            vector search engine. You can turn neural search on and off to
            compare the result with regular full-text search. Try to use startup
            description to find similar ones.
          </Text>

          <Image src="/workflow.svg" />
          <Text size="lg" color="dimmed" className={classes.description}>
            You will discover that given a short query - a full-text search
            provides more precise results but lower recall when a neural search
            may find close and fuzzy matches. For similarity search and longer
            queries - full-text search struggles to catch the meaning of the
            query and return noisy results, while neural search finds better and
            semantically closer results.
          </Text>
          <Button
            className={classes.modalBtnInner}
            radius={30}
            size={"md"}
            variant="filled"
            color="Primary.2"
            onClick={close}
          >
            Get started
          </Button>
        </Modal.Body>
      </Modal>
    </MantineHeader>
  );
}
