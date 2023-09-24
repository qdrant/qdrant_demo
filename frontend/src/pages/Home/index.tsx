import { Main } from "@/components/MainSection";
import { CustomHeader } from "@/components/CustomHeader";
import { Box } from "@mantine/core";

export default function Home() {
  return (
    <Box>
      <CustomHeader />
      <Main />
    </Box>
  );
}
