import { createStyles, rem } from "@mantine/core";

export const useStyles = createStyles((theme) => ({
  wrapper: {
    position: "relative",
    paddingTop: rem(120),
    paddingBottom: rem(80),

    [theme.fn.smallerThan("sm")]: {
      paddingTop: rem(80),
      paddingBottom: rem(60),
    },
  },

  inner: {
    position: "relative",
    zIndex: 1,
  },
  title: {
    textAlign: "center",
    fontWeight: 700,
    fontSize: rem(40),
    letterSpacing: -1,
    marginBottom: theme.spacing.xs,
    [theme.fn.smallerThan("xs")]: {
      fontSize: rem(30),
    },
  },

  highlight: {
    color:
      theme.colors[theme.primaryColor][2],
  },

  description: {
    textAlign: "center",

    [theme.fn.smallerThan("xs")]: {
      fontSize: theme.fontSizes.md,
    },
  },

  controls: {
    marginTop: theme.spacing.lg,
    display: "flex",
    justifyContent: "center",
    [theme.fn.smallerThan("xs")]: {
      flexDirection: "column",
    },
  },

  control: {
    "&:not(:first-of-type)": {
      marginLeft: theme.spacing.md,
    },

    [theme.fn.smallerThan("xs")]: {
      height: rem(42),
      fontSize: theme.fontSizes.md,
      "&:not(:first-of-type)": {
        marginTop: theme.spacing.md,
        marginLeft: 0,
      },
    },
  },
  inputRightSection:{
    display: "flex",
    alignItems: "center",
    gap: theme.spacing.xs,
    paddingLeft: 10,
    paddingRight: 10,
    marginRight: 5,
    zIndex: 1,
    backgroundColor: "white",
  },
  inputArea: {
    width: "100%",
    [theme.fn.smallerThan("xs")]: {
      height: rem(28),
      fontSize: theme.fontSizes.md,
    },
    "& .mantine-TextInput-rightSection	":{
      width: "auto",
    }
  },
  viewResult:{
    paddingTop: theme.spacing.md,
  }
}));
