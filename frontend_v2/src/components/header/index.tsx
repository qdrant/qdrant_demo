import {
  createStyles,
  Header as MantineHeader,
  Group,
  ActionIcon,
  Container,
  rem,
  Tooltip,
} from "@mantine/core";
import { IconBrandGithub, IconBook2, IconSettings } from "@tabler/icons-react";
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

  social: {
    width: rem(260),

    [theme.fn.smallerThan("sm")]: {
      width: "auto",
      marginLeft: "auto",
    },
  },
}));

export default function Header() {
  const { classes } = useStyles();

  return (
    <MantineHeader height={56} mb={120}>
      <Container className={classes.inner}>
        <Logo size={35} />

        <Group spacing={3} className={classes.social} position="right" noWrap>
          <Tooltip label="View Code" position="bottom" withArrow>
            <ActionIcon
              size="lg"
              color="pink"
              variant="light"
              component="a"
              href="https://github.com/qdrant/qdrant_demo"
              target="_blank"
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
            >
              <IconBook2 size="1.1rem" stroke={1.5} />
            </ActionIcon>
          </Tooltip>
          <Tooltip label="Settings" position="bottom" withArrow>
            <ActionIcon size="lg" color="pink" variant="light">
              <IconSettings size="1.1rem" stroke={1.5} />
            </ActionIcon>
          </Tooltip>
        </Group>
      </Container>
    </MantineHeader>
  );
}
