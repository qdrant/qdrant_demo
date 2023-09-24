import { MantineProvider, createEmotionCache } from '@mantine/core';

import type { FC, ReactNode } from 'react';
import theme  from './index';

const myCache = createEmotionCache({ key: 'mantine' });

type MantineProps = {
	children?: ReactNode;
};

const Mantine: FC<MantineProps> = (props) => {
	const { children } = props;

	return (
		<MantineProvider withGlobalStyles withNormalizeCSS theme={theme} emotionCache={myCache}>
        {children}
		</MantineProvider>
	);
};

export default Mantine;
