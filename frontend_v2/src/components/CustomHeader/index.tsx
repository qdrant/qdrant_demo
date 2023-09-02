import {
  createStyles,
  Header as MantineHeader,
  Group,
  ActionIcon,
  Container,
  rem,
  Tooltip,
} from "@mantine/core";
import { IconBrandGithub, IconBook2 } from "@tabler/icons-react";
import { Logo } from "../Logo";

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
}));

export function CustomHeader() {
  const { classes } = useStyles();
  return (
    <MantineHeader height={56} bg={"Neutral.0"} fixed sx={{
      zIndex: 100,
    }}  >
      <Container className={classes.inner}>
        <Logo size={35} />

        <Group spacing={10} className={classes.links} position="right" noWrap>
          <Tooltip label="View Code" position="bottom" withArrow>
            <ActionIcon
              size="lg"
              color="pink"
              variant="light"
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
              color="pink"
              variant="light"
              component="a"
              href="https://github.com/qdrant/qdrant_demo/blob/master/README.md"
              target="_blank"
              className={classes.link}
            >
              <IconBook2 size="1.1rem" stroke={1.5} />
            </ActionIcon>
          </Tooltip>
          {/* <Tooltip label="View Docs" position="bottom" withArrow>
            <ActionIcon
              size="lg"
              color="pink"
              variant="light"
              component="a"
              href="https://github.com/qdrant/qdrant_demo/blob/master/README.md"
              target="_blank"
              className={classes.link}
            >
              <IconInfoCircle size="1.1rem" stroke={1.5} />
            </ActionIcon>
          </Tooltip> */}
        </Group>
      </Container>
    </MantineHeader>
  );
}
