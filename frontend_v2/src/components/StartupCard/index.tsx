import {
  Card,
  Image,
  Text,
  Badge,
  Button,
  Group,
  createStyles,
  Tooltip,
  ActionIcon,
  Box,
  rem,
} from "@mantine/core";
import { IconExternalLink } from "@tabler/icons-react";
import DOMPurify from "dompurify";

type StartupCardProps = {
  data: {
    Index: number;
    _1: number;
    name: string;
    images: string;
    alt: string;
    description: string;
    link: string;
    city: string;
  };
  onClickFindSimilar: (data: string) => void;
};
export const useStyles = createStyles(() => ({
  card: {
    height: "100%",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    transition: "transform .3s ease-in-out",
  },
}));

export function StartupCard(prop: StartupCardProps) {
  const data = prop.data;
  const onClickFindSimilar = prop.onClickFindSimilar;
  const { classes } = useStyles();
  return (
    <Card
      shadow="sm"
      padding="lg"
      radius="md"
      withBorder
      key={data.Index}
      className={classes.card}
    >
      <Card.Section>
        <Image
          h={"100%"}
          src={data.images}
          withPlaceholder
          alt={"No results found."}
          p={10}
          radius="md"
          placeholder={
            <Image src={"./error.gif"} alt="No results found." radius="md" />
          }
          sx={{
            "& .mantine-Image-placeholder": {
              backgroundColor: "white",
              position: "relative",
              marginTop: "-27px",
            },
            "& .mantine-Image-image": {
              border: "1px solid #e3e3e3",
            },
          }}
        />
      </Card.Section>

      <Box mt="md" mb="xs">
        <Text weight={500} size={rem(25)}>
          {data.name}
        </Text>
        <Badge color="blue" variant="light">
          {data.city}
        </Badge>
      </Box>

      <Text
        size="sm"
        color="dimmed"
        dangerouslySetInnerHTML={{
          __html: DOMPurify.sanitize(
            data.description.length > 100
              ? data.description.substring(0, 80) + "..."
              : data.description
          ),
        }}
      />

      <Group position="apart" mt="md" mb="xs">
        <Button
          variant="light"
          color="pink"
          onClick={() => {
            onClickFindSimilar(data.description);
          }}
        >
          Find Similar
        </Button>
        <Tooltip label="Visit Website" position="bottom" withArrow>
          <ActionIcon
            size="lg"
            color="pink"
            variant="light"
            component="a"
            href={data.link}
            target="_blank"
          >
            <IconExternalLink size="1.1rem" stroke={1.5} />
          </ActionIcon>
        </Tooltip>
      </Group>
    </Card>
  );
}
