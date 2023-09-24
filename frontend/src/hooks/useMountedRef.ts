import { useRef, useEffect } from 'react';

const useMountedRef = () => {
	const mounted = useRef(false);

	useEffect(() => {
		mounted.current = true;

		return () => {
			mounted.current = false;
		};
	}, []);

	return mounted;
};

export default useMountedRef;
