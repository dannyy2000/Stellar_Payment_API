import remarkGfm from 'remark-gfm';
import { MDXRemoteSerializeOptions } from 'next-mdx-remote/rsc';
import rehypePrismPlus from 'rehype-prism-plus';

export const mdxOptions: MDXRemoteSerializeOptions = {
  mdxOptions: {
    remarkPlugins: [remarkGfm],
    rehypePlugins: [
      [rehypePrismPlus, { defaultLanguage: 'bash' }],
    ],
  },
};
