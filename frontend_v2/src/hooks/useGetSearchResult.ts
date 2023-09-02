import { getSearchResult } from '@/api/search';
import { StatusCodes } from 'http-status-codes';
import useMountedState from './useMountedState';

export type searchResponse = {
	result: {
		Index: number;
		_1: number;
		name: string;
		images: string;
		alt: string;
		description: string;
		link: string;
		city: string;
	}[];
};
export const useGetSearchResult = () => {
	const [data, setData] = useMountedState<searchResponse | null>(null);
	const [error, setError] = useMountedState<string | null>(null);
	const [loading, setLoading] = useMountedState<boolean>(false);

	const getSearch = async (query: string,neural?:boolean) => {
		try {
			setLoading(true);
			setError(null);
			const res = await getSearchResult({ query,neural });

			switch (res.status) {
				case StatusCodes.OK: {
					const searchRes = res.data;
					setData(searchRes);
					break;
				}
				default: {
					setError('Failed to get Search Result');
				}
			}
		} catch {
			setError('Failed to get Search Result');
		} finally {
			setLoading(false);
		}
	};

	const resetData = () => {
		setData(null);
	};

	return { data, error, loading, getSearch, resetData };
};
