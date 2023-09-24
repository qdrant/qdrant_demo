import { useState, useCallback, SetStateAction } from 'react';

import useMountedRef from './useMountedRef';

const useMountedState = <T>(value: T | (() => T)): [T, (newState: SetStateAction<T>) => void] => {
	const mountedRef = useMountedRef();
	const [state, setState] = useState<T>(value);

	const setMountedState = useCallback(
		(newValue: SetStateAction<T>) => {
			if (mountedRef.current) {
				setState(newValue);
			}
		},
		[mountedRef],
	);

	return [state, setMountedState];
};

export default useMountedState;
