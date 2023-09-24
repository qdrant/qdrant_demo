import {
  Image,
  Text,
  Badge,
  Button,
  Group,
  createStyles,
  Grid,
} from "@mantine/core";
import { IconExternalLink } from "@tabler/icons-react";
import DOMPurify from "dompurify";

type StartupCardProps = {
  Index: string;
  name: string;
  images: string;
  alt: string;
  description: string;
  link: string;
  city: string;
  onClickFindSimilar: (data: string) => void;
};

const useStyles = createStyles((theme) => ({
  card: {
    backgroundColor:
      theme.colorScheme === "dark" ? theme.colors.dark[7] : theme.white,
    borderRadius: theme.radius.md,
    boxShadow: theme.shadows.md,
    padding: theme.spacing.md,
    marginBottom: theme.spacing.md,
  },

  title: {
    fontWeight: 700,
    fontFamily: `${theme.fontFamily}`,
    lineHeight: 1.2,
    color:theme.colors.Neutral[8]
  },

  body: {},
  imageBox: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  btnBox: {
    display: "flex",
  },
}));

export function StartupCard({
  images,
  city,
  name,
  description,
  link,
  onClickFindSimilar,
}: StartupCardProps) {
  const { classes } = useStyles();
  return (
    <Grid className={classes.card}>
      <Grid.Col xs={2} className={classes.imageBox}>
        <Image
          src={images}
          withPlaceholder
          alt={"No results found."}
          radius="md"
          sx={{
            "& .mantine-Image-image": {
              border: "1px solid #e3e3e3",
            },
          }}
        />
      </Grid.Col>
      <Grid.Col xs={10} >
        <Grid sx={{
            display:"flex",
            alignContent:"center",
            height:"100%"
    
        }}>
          <Grid.Col sm={6} md={7} >
            <Badge color="blue" variant="light">
              {city}
            </Badge>
            <Text
              className={classes.title}
              size="lg"
              weight={700}
              style={{ marginTop: 10 }}
            >
              {name}
            </Text>
            <Text
              size="sm"
              weight={400}
              style={{ marginTop: 10 }}
              color="Neutral.6"
              dangerouslySetInnerHTML={{
                __html: DOMPurify.sanitize(
                  description.length > 200
                    ? description.substring(0, 180) + "..."
                    : description
                ),
              }}
            />
          </Grid.Col>
          <Grid.Col sm={6} md={5} className={classes.btnBox}>
            <Group noWrap position="center" h={"100%"}>
              <Button
                variant="subtle"
                radius={"xl"}
                color="Neutral.8"
                onClick={() => onClickFindSimilar(description)}
              >
                Find Similar
              </Button>
              <Button
                variant="outline"
                color="Neutral.8"
                href={link}
                target="_blank"
                component="a"
                radius={"xl"}
                sx={{
                  border: "1px solid #DCE4FA",
                }}
                rightIcon={<IconExternalLink />}
              >
                View Website
              </Button>
            </Group>
          </Grid.Col>
        </Grid>
      </Grid.Col>
    </Grid>
  );
}
