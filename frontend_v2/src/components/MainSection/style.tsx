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
    color: theme.colors.Neutral[7],
    textAlign: "center",
    fontWeight: 700,
    fontSize: "2.5rem",
    fontStyle: "normal",
    lineHeight: "3rem",
  },

  highlight: {
    color: theme.colors[theme.primaryColor][2],
  },

  description: {
    paddingTop: theme.spacing.xs,
    textAlign: "center",
    color: theme.colors.Neutral[6],
    fontSize: theme.other.paragraph.sizes.P18.fontSize,
    lineHeight: theme.other.paragraph.sizes.P18.lineHeight,
    fontWeight: theme.other.paragraph.sizes.P18.fontWeight,
  },

  controls: {
    textAlign: "center",
  },

  control: {
    backgroundColor: theme.colors.Neutral[1],
    marginTop: theme.spacing.xl,
    border: `1px solid ${theme.colors.Neutral[2]}`,
  },
  inputRightSection: {},
  inputArea: {
    marginTop: theme.spacing.xl,
    "& .mantine-TextInput-input": {
      border: `1px solid ${theme.colors.Neutral[2]}`,
      color: theme.colors.Neutral[6],
      "::-webkit-input-placeholder": {
        color: theme.colors.Neutral[6],
      },
    },
  },
  viewResult: {
    paddingTop: theme.spacing.md,
  },
}));
